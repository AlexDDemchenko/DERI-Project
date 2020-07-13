import tweepy
import datetime
import sys
import csv

consumerKey = "UJc1xpDNnVvxjQszKR5VGjxH6"
consumerSecret = "y0ZE4PsnhCwcuSyRVVGVSWcy2S7rl4SKHywMiYK8VFUC9nv1NY"
accessToken = "1142057661384581120-cWOpHesXKC8tgPsCWMm7oP7XE5VDVH"
accessTokenSecret = "ho3RAWS1l8iTcvVcCLwJFz7FKjDvLplERKrOrQdlSUD8X"


auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)


# todo: you'll want to save the access codes so you don't need the
# user to grant you access the next time:
# auth.access_token.key
# auth.access_token.secret

# connect to api as user and print out their timeline
api = tweepy.API(auth)
with open('trump.csv', 'w', encoding="utf-8") as f:
    writer = csv.writer(f)
    for tweet in api.user_timeline(screen_name = "@realDonaldTrump",count=2000000):
        #print(tweet.user.location)
        #print (tweet.text + " " + str(tweet.created_at) )
        writer.writerows(str(tweet.text).replace("\n",""))
        writer.writerows(str(tweet.created_at).replace("\n",""))

f.close()
