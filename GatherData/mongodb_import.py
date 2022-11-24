from config import PASS, LOGIN
import certifi
from pymongo import MongoClient
from data_gathering import get_tweets

# Add Certificate for connection

ca = certifi.where()

#TODO Create MongoSB cluster
client = MongoClient(f"mongodb+srv://{LOGIN}:{PASS}@cluster0.psdqkii.mongodb.net/test", tlsCAFile=ca)
db = client['topic']

get_tweets()