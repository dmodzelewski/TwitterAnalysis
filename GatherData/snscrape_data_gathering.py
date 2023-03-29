import time

import geocoder
import snscrape.modules.twitter as sntwitter
import pandas as pd
import tweepy
from config import *
from datetime import datetime
import itertools
import aiohttp
import asyncio

# Dictionaries are 585714 times faster than lists when it comes to 10 milion records


client = tweepy.Client(BEARER_TOKEN)


# Configure API
def api():
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


# Get location of trends by woeid code
# Get most popular location with english language by woeid code
# https://www.woeids.com/
# return list of most popular trens
def get_trends(api):
    popular_cities = {"new_york": 2459115, "london": 44418, "sydney": 1105779}
    trends = []
    for woeid in popular_cities.values():
        trends.append([trend["name"] for trend in api.get_place_trends(woeid)[0]["trends"][:3]])
    trends = list(set(itertools.chain.from_iterable(trends)))
    return trends


def get_tweets(topic, start_date, end_date=datetime.today().strftime("%Y-%m-%d"), limit=100):
    twitter_dict = {"created_at": [], "id": [], "text": [], "screen_name": [], "name": [],
                    "retweet_count": [], "like_count": [], "quote_count": [], "view_count": [],
                    "user_created": [], "user_favourites_count": [], "user_followers_count": [],
                    "user_friends_count": [], "user_statuses_count": [], "verified": [], "topic": []}
    query = f"({topic}) lang:en until:{end_date} since:{start_date}"
    for l, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items(), 1):
        if l > limit:
            break
        if l % 1000 == 0:
            print("loading")
        twitter_dict["created_at"].append(tweet.date)
        twitter_dict["id"].append(tweet.id)
        twitter_dict["text"].append(tweet.rawContent)
        twitter_dict["topic"].append(topic)
        twitter_dict["retweet_count"].append(tweet.retweetCount)
        twitter_dict["like_count"].append(tweet.likeCount)
        twitter_dict["quote_count"].append(tweet.quoteCount)
        twitter_dict["screen_name"].append(tweet.user.username)
        twitter_dict["view_count"].append(tweet.viewCount)
        twitter_dict["user_created"].append(tweet.user.created)
        twitter_dict["user_favourites_count"].append(tweet.user.favouritesCount)
        twitter_dict["user_followers_count"].append(tweet.user.followersCount)
        twitter_dict["name"].append(tweet.user.displayname)
        twitter_dict["user_friends_count"].append(tweet.user.friendsCount)
        twitter_dict["user_statuses_count"].append(tweet.user.statusesCount)
        twitter_dict["verified"].append(tweet.user.verified)
    return pd.DataFrame.from_dict(twitter_dict)
