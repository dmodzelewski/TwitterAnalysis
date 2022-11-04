import tweepy
from config import *

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = "Ukraina has:hashtags	 lang:pl -is:retweet -has:media"

response = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'lang'])
list_ = []
for tweet in response.data:
    list_.append(tweet.text)

print(list_)