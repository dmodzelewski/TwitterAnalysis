from datetime import datetime
from config import PASS, LOGIN
import certifi
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Add Certificate for connection
ca = certifi.where()

#TODO Create MongoSB cluster
client = MongoClient(f"mongodb+srv://{LOGIN}:{PASS}@hurtowniedanych.oqbfe.mongodb.net", tlsCAFile=ca)
db = client['search_laptops']
