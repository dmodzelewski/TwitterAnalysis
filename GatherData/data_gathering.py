import tweepy
from config import *

auth = tweepy.OAuthHandler(API_KEY,API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#Get all trends from Poland
availiable_trends = api.get_place_trends(id=526363)

print(availiable_trends)
print(len(availiable_trends))

#Get tweets

# query = "#Inflacja lang:pl -is:retweet -has:images"
# response = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'lang'])

