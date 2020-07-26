"""
Title: Structured data classification from scratch
Author: [fchollet](https://twitter.com/fchollet)
Date created: 2020/06/09
Last modified: 2020/06/09
Description: Binary classification of structured data including numerical and categorical features.
"""
"""
## Introduction
This example demonstrates how to do structured data classification, starting from a raw
CSV file. Our data includes both numerical and categorical features. We will use Keras
preprocessing layers to normalize the numerical features and vectorize the categorical
ones.
Note that this example should be run with TensorFlow 2.3 or higher, or `tf-nightly`.
### The dataset
[Our dataset](https://archive.ics.uci.edu/ml/datasets/heart+Disease) is provided by the
Cleveland Clinic Foundation for Heart Disease.
It's a CSV file with 303 rows. Each row contains information about a patient (a
**sample**), and each column describes an attribute of the patient (a **feature**). We
use the features to predict whether a patient has a heart disease (**binary
classification**).
Here's the description of each feature:
Column| Description| Feature Type
------------|--------------------|----------------------
Age | Age in years | Numerical
Sex | (1 = male; 0 = female) | Categorical
CP | Chest pain type (0, 1, 2, 3, 4) | Categorical
Trestbpd | Resting blood pressure (in mm Hg on admission) | Numerical
Chol | Serum cholesterol in mg/dl | Numerical
FBS | fasting blood sugar in 120 mg/dl (1 = true; 0 = false) | Categorical
RestECG | Resting electrocardiogram results (0, 1, 2) | Categorical
Thalach | Maximum heart rate achieved | Numerical
Exang | Exercise induced angina (1 = yes; 0 = no) | Categorical
Oldpeak | ST depression induced by exercise relative to rest | Numerical
Slope | Slope of the peak exercise ST segment | Numerical
CA | Number of major vessels (0-3) colored by fluoroscopy | Both numerical & categorical
Thal | 3 = normal; 6 = fixed defect; 7 = reversible defect | Categorical
Target | Diagnosis of heart disease (1 = true; 0 = false) | Target
"""

"""
## Setup
"""

import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers






"""
## Preparing the data
Let's download the data and load it into a Pandas dataframe:
"""

file_url = r"C:\Users\Administrator\Desktop\DERI\followers\output.csv"
dataframe = pd.read_csv(file_url)

"""
The dataset includes 303 samples with 14 columns per sample (13 features, plus the target
label):
"""

dataframe.shape

"""
Here's a preview of a few samples:
"""

dataframe.head()

"""
The last column, "target", indicates whether the patient has a heart disease (1) or not
(0).
Let's split the data into a training and validation set:
"""

val_dataframe = dataframe.sample(frac=0.15, random_state=1337)
train_dataframe = dataframe.drop(val_dataframe.index)

print(
    "Using %d samples for training and %d for validation"
    % (len(train_dataframe), len(val_dataframe))
)

"""
Let's generate `tf.data.Dataset` objects for each dataframe:
"""


def dataframe_to_dataset(dataframe):
    dataframe = dataframe.copy()
    labels = dataframe.pop("Bot_or_Not")
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    ds = ds.shuffle(buffer_size=len(dataframe))
    return ds


train_ds = dataframe_to_dataset(train_dataframe)
val_ds = dataframe_to_dataset(val_dataframe)

"""
Each `Dataset` yields a tuple `(input, target)` where `input` is a dictionary of features
and `target` is the value `0` or `1`:
"""

for x, y in train_ds.take(1):
    print("Input:", x)
    print("Target:", y)

"""
Let's batch the datasets:
"""

train_ds = train_ds.batch(32)
val_ds = val_ds.batch(32)

"""
## Feature preprocessing with Keras layers
The following features are categorical features encoded as integers:
-'Profile picture contains face?'
-'Bot Score'
We will encode these features using **one-hot encoding** using the `CategoryEncoding()`
layer.
We also have a categorical feature encoded as a string: `thal`. We will first create an
index of all possible features using the `StringLookup()` layer, then we will one-hot
encode the output indices using a `CategoryEncoding()` layer.
Finally, the following feature are continuous numerical features:
-'followers'
-'following'
-'creation date'
-'number of tweets'
-'Retweet Ratio'
-'Tweets Per Day'

For each of these features, we will use a `Normalization()` layer to make sure the mean
of each feature is 0 and its standard deviation is 1.
Below, we define 3 utility functions to do the operations:
- `encode_numerical_feature` to apply featurewise normalization to numerical features.
- `encode_string_categorical_feature` to first turn string inputs into integer indices,
then one-hot encode these integer indices.
- `encode_integer_categorical_feature` to one-hot encode integer categorical features.
"""

from tensorflow.keras.layers.experimental.preprocessing import Normalization
from tensorflow.keras.layers.experimental.preprocessing import CategoryEncoding
from tensorflow.keras.layers.experimental.preprocessing import StringLookup


def encode_numerical_feature(feature, name, dataset):
    # Create a Normalization layer for our feature
    normalizer = Normalization()

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the statistics of the data
    normalizer.adapt(feature_ds)

    # Normalize the input feature
    encoded_feature = normalizer(feature)
    return encoded_feature


def encode_string_categorical_feature(feature, name, dataset):
    # Create a StringLookup layer which will turn strings into integer indices
    index = StringLookup()

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the set of possible string values and assign them a fixed integer index
    index.adapt(feature_ds)

    # Turn the string input into integer indices
    encoded_feature = index(feature)

    # Create a CategoryEncoding for our integer indices
    encoder = CategoryEncoding(output_mode="binary")

    # Prepare a dataset of indices
    feature_ds = feature_ds.map(index)

    # Learn the space of possible indices
    encoder.adapt(feature_ds)

    # Apply one-hot encoding to our indices
    encoded_feature = encoder(encoded_feature)
    return encoded_feature


def encode_integer_categorical_feature(feature, name, dataset):
    # Create a CategoryEncoding for our integer indices
    encoder = CategoryEncoding(output_mode="binary")

    # Prepare a Dataset that only yields our feature
    feature_ds = dataset.map(lambda x, y: x[name])
    feature_ds = feature_ds.map(lambda x: tf.expand_dims(x, -1))

    # Learn the space of possible indices
    encoder.adapt(feature_ds)

    # Apply one-hot encoding to our indices
    encoded_feature = encoder(feature)
    return encoded_feature


"""
## Build a model
With this done, we can create our end-to-end model:
"""

# Categorical features encoded as integers
Profile_pic = keras.Input(shape=(1,), name="Profile_picture", dtype="int64")
Bot_Score = keras.Input(shape=(1,), name="Bot_Score", dtype="int64")


# Categorical feature encoded as string
#thal = keras.Input(shape=(1,), name="thal", dtype="string")

# Numerical features
followers = keras.Input(shape=(1,), name="followers")
following = keras.Input(shape=(1,), name="following")
creation_date = keras.Input(shape=(1,), name="creation_date")
number_of_tweets = keras.Input(shape=(1,), name="number_of_tweets")
Retweet_Ratio = keras.Input(shape=(1,), name="Retweet_Ratio")
Tweets_Per_Day = keras.Input(shape=(1,), name="Tweets_Per_Day")

all_inputs = [
    followers,
    following,
    creation_date,
    number_of_tweets,
    Retweet_Ratio,
    Profile_pic,
    Tweets_Per_Day,
    Bot_Score,
]

# Integer categorical features
Profile_pic_encoded = encode_integer_categorical_feature(Profile_pic, "Profile_picture", train_ds)
Tweets_Per_Day_encoded = encode_integer_categorical_feature(Tweets_Per_Day, "Bot_Score", train_ds)


# String categorical features
#thal_encoded = encode_string_categorical_feature(thal, "thal", train_ds)

# Numerical features
followers_encoded = encode_numerical_feature(followers, "followers", train_ds)
following_encoded = encode_numerical_feature(following, "following", train_ds)
creation_date_encoded = encode_numerical_feature(creation_date, "creation_date", train_ds)
number_of_tweets_encoded = encode_numerical_feature(number_of_tweets, "number_of_tweets", train_ds)
Retweet_Ratio_encoded = encode_numerical_feature(Retweet_Ratio, "Retweet_Ratio", train_ds)
Bot_Score_encoded = encode_numerical_feature(Bot_Score, "Tweets_Per_Day", train_ds)

all_features = layers.concatenate(
    [
        followers_encoded,
        following_encoded,
        creation_date_encoded,
        number_of_tweets_encoded,
        Retweet_Ratio_encoded,
        Profile_pic_encoded,
        Tweets_Per_Day_encoded,
        Bot_Score_encoded,
    ]
)
x = layers.Dense(32, activation="relu")(all_features)
x = layers.Dropout(0.5)(x)
output = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(all_inputs, output)
model.compile("adam", "binary_crossentropy", metrics=["accuracy"])

"""
Let's visualize our connectivity graph:
"""

# `rankdir='LR'` is to make the graph horizontal.
#keras.utils.plot_model(model, show_shapes=True, rankdir="LR")

"""
## Train the model
"""

model.fit(train_ds, epochs=50, validation_data=val_ds)

"""
We quickly get to 80% validation accuracy.
"""

"""
## Inference on new data
To get a prediction for a new sample, you can simply call `model.predict()`. There are
just two things you need to do:
1. wrap scalars into a list so as to have a batch dimension (models only process batches
of data, not single samples)
2. Call `convert_to_tensor` on each feature
"""

sample = {
    "followers": 100,
    "following": 50,
    "creation_date": 2010,
    "number_of_tweets": 800,
    "Retweet_Ratio": .3,
    "Profile_picture": 1,
    "Bot_Score": 5,
}

input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
predictions = model.predict(input_dict)

print(
    "This twitter account has a %.1f percent chance of being a bot." % (100 * predictions[0][0],)
)
