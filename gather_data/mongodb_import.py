from config import PASS, LOGIN
import certifi
from pymongo import MongoClient
from snscrape_data_gathering import *
from datetime import date, timedelta

# Add Certificate for connection

ca = certifi.where()

client = MongoClient(f"mongodb+srv://{LOGIN}:{PASS}@cluster0.psdqkii.mongodb.net/Twitter", tlsCAFile=ca)
db = client["Test"]
collection = db["Test"]


# List of all trends


def trending_tweets():
    trends = get_trends(api())
    for i in range(len(trends)):
        print(f"Getting tweets from topic: {trends[i]}")
        tweets = get_tweets(trends[i], start_date="2023-02-24", limit=1000)
        print("Saving data to MongoDB")
        try:
            collection.insert_many(tweets.to_dict("records"))
        except TypeError:
            pass


def pick_trends(trend, start, end):
    print(f"Getting tweets from topic: {trend}")
    tweets = get_tweets(trend, start_date=f"{start}", end_date=f"{end}", limit=100)
    print("Saving to mongo db")
    try:
        collection.insert_many(tweets.to_dict("records"))
    except TypeError:
        pass


# Get all tweets from popular topics
# for y in range(2022, 2023):
#     for m in range(1, 13):
#         for d in range(1, 28):
#             pick_trends("Ukraine war", y, m, d)
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


trending_tweets()