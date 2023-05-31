import pandas as pd
import tweepy
from config import *
import geocoder

loc = "Poland"
twitter_dict = {"created_at": [], "id": [], "text": [], "screen_name": [], "name": [],
                "retweet_count": [], "favourites_count": [], "friends_count": [], "followers_count": [],
                "statuses_count": [], "verified": [], "user_created_at": [], "hashtag": []}

client = tweepy.Client(BEARER_TOKEN)


# Configure API
def api():
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


# Get location of trends by woeid code
def get_trends(api, loc):
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.get_place_trends(44418)
    return trends[0]["trends"]


def extract_hashtags(trends):
    hashtags = [trend["name"] for trend in trends if "#" in trend["name"]]
    return hashtags


def extract__without_hashtags(trends):
    hashtags = [trend["name"] for trend in trends if "#" not in trend["name"]]
    return hashtags


def get_n_tweets(api, query_topic, n, lang=None):
    for status in tweepy.Cursor(
            api.search_tweets,
            q=f"{query_topic} -is:retweet -has:images",
            lang=lang,
            result_type="mixed"
    ).items(n):
        twitter_dict["created_at"].append(str(status.created_at))
        twitter_dict["id"].append(status.id)
        twitter_dict["text"].append(status.text)
        twitter_dict["screen_name"].append(status.user.screen_name)
        twitter_dict["name"].append(status.user.name)
        twitter_dict["retweet_count"].append(int(status.retweet_count))
        twitter_dict["favourites_count"].append(int(status.user.favourites_count))
        twitter_dict["friends_count"].append(status.user.friends_count)
        twitter_dict["followers_count"].append(status.user.followers_count)
        twitter_dict["user_created_at"].append(status.user.created_at)
        twitter_dict["statuses_count"].append(status.user.statuses_count)
        twitter_dict["verified"].append(status.user.verified)
        twitter_dict["hashtag"].append(query_topic)
        print("loading")
    return pd.DataFrame.from_dict(twitter_dict)


# Get recent trends
def get_tweets():
    trends = get_trends(api(), loc)
    hashtags = extract_hashtags(trends)
    no_hashtags = extract__without_hashtags(trends)
    hashtag = hashtags[1]
    print(hashtag)
    print(no_hashtags)
    # tweets = get_n_tweets(api(), hashtag, 1, "en")

    # return tweets
