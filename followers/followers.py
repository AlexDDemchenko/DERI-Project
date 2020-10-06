from tweepy import OAuthHandler
import numpy as np
import secrets
import tweepy
from datetime import date
import datetime
import pandas as pd
import os
import cv2
import io
import requests
from PIL import Image
with open('input.txt', 'r') as f:
    name = f.read()
    f.close()
auth = OAuthHandler(secrets.CONSUMER_KEY,secrets.CONSUMER_SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN,secrets.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
today = date.today()
account_count = 0
usernames = []
follow_c = []
friends = []
favorites = []
num_of_tweets = []
def_profile = []
profile_pic = []
verified = []
final_bot_score = []
names = name.split()
for name in names:
    account_count += 1
    print("Account No.")
    print(account_count)
    try:
        bot_score = 0
        user = api.get_user(name)
        usernames.append(name)
        follow_c.append(user.followers_count)
        friends.append(user.friends_count)
        favorites.append(user.favourites_count)
        num_of_tweets.append(user.statuses_count)
        def_profile.append(user.default_profile)
        profile_pic.append(user.default_profile_image)
        verified.append(user.verified)
        if user.friends_count > 5000:
            bot_score += 5
        elif user.friends_count > 1000:
            bot_score += 3
        if user.statuses_count > 300000:
            bot_score += 5
        elif user.statuses_count > 100000:
            bot_score += 3
        if user.default_profile == True:
            bot_score += 8
        if user.default_profile_image == True:
            bot_score += 8
        if user.verified == True:
            bot_score = 0
        final_bot_score.append(bot_score)
    except:
        print("username does not exist")
        pass
data = {'username' : usernames,
        'followers_count': follow_c,
        'friends_count' : friends,
        'favorites_count' : favorites,
        'statuses_count' : num_of_tweets,
        'default_profile' : def_profile,
        'default_profile_image' : profile_pic,
        'verified' : verified,
        'Bot Score' : final_bot_score}
df = pd.DataFrame(data)
if os.path.exists('output.csv'):
    os.remove('output.csv')
df.to_csv('output.csv', index = False)








