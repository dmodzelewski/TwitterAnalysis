import pandas as pd
import tweepy
from config import *
import geocoder

loc = "Poland"
twitter_dict = {"created_at": [], "id": [], "text": [], "screen_name": [], "name": [],
                "retweet_count": [], "favorite_count": []}
client = tweepy.Client(BEARER_TOKEN)


# Configure API
def api():
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


# Get location of trends
def get_trends(api, loc):
    g = geocoder.osm(loc)

    closest_loc = api.closest_trends(g.lat, g.lng)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
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
        twitter_dict["retweet_count"].append(status.retweet_count)
        twitter_dict["favorite_count"].append(status.favorite_count)
        print("loading")
    return pd.DataFrame.from_dict(twitter_dict)


# Get recent trends
def get_tweets():
    trends = get_trends(api(), loc)
    hashtags = extract_hashtags(trends)
    no_hashtags = extract__without_hashtags(trends)
    hashtag = hashtags[0]
    tweets = get_n_tweets(api(), hashtag, 10, "en")

    return tweets
# Get tweets

# query = "#Inflacja lang:pl -is:retweet -has:images"
# response = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'lang'])
