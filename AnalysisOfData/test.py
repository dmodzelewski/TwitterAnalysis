from nltk import TweetTokenizer, SnowballStemmer
from nltk.corpus import stopwords
from pymongo import MongoClient
from spellchecker import SpellChecker

from GatherData.config import PASS, LOGIN

import certifi

import numpy as np
import pandas as pd
import re
import nltk
import spacy
import string
import openpyxl
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer

chat_words_str = """
DM=Direct message
CT=Cuttweet
RT=Retweet
PRT=Partial retweet
MT=Modified tweet
PRT=Please retweet
HT=Hat tip
CC=Carbon-copy
CX=Correction
EM=Email Marketing
SEO=Search Engine Optimization
SROI=Social Return on Investment
SN=Social Network
YT=YouTube
UGC=User-Generated Content
SMO=Social Media Optimization
FB=Facebook
LI=LinkedIn
SM=Social Media
SMM=Social Media Marketing
EZine=Electronic Magazine
BGD=Background
CD9=Code 9, parents are around
BTW=By the way
AB=About
ABT=About
DD=Dear daughter
AFAIK=far as I know
AYFKMWTS=Are you f—ing kidding me with this s—?
BR=Best regards
CHK=Check
CUL8R=See you later
DP=used to mean “profile pic”
FML=F— my life
FUBAR=F—ed up beyond all repair (slang from the US Military)
BBFN=Bye for now
B4=Before
DS=Dear son
FF=Follow Friday
EMA=Email address
DYK=Do you know
F2F=Face to face
FTF=Face to face
HAGN=Have a good night
DF=Dear fiancé
DAM=Don’t annoy me
FFS=For F—‘s Sake
EM=Email
EML=Email
FOTD=Find of the day
FTW=For the win, F— the world
FWIW=For what it’s worth
HTH=Hope that helps
GMAFB=Give me a f—ing break
HAND=Have a nice day
ICYMI=In case you missed it
GTFOOH=Get the f— out of here
GTS=Guess the song
HOTD=Headline of the day
IIRC=If I remember correctly
KYSO=Knock your socks off
KK=Kewl kewl, or ok, got it
HT=Head through
IC=I see
IDK=I don’t know
LHH=hella hard
ZOMG=OMG to the max
IMHO=In my humble opinion
NFW=No f—ing way
ORLY=Oh, really?
YOYO=You’re on your own
LMAO=Laughing my ass off
IRL=In real life
JK=Just kidding
JV=Joint venture
LO=Little One
LOL=Laugh out loud
MM=Music Monday
LMK=Let me know
TY=Thank you
SRS=Serious
STF=Shut the f—
STFU=Shut the f— up!
TL=Timeline
TYIA=Thank you in advance
TT=Trending topic
TYVW=Thank you very much
BRB=Be Right Back
AFAIK=As Far As I Know
AFK=Away From Keyboard
ASAP=As Soon As Possible
ATK=At The Keyboard
ATM=At The Moment
A3=Anytime, Anywhere, Anyplace
BAK=Back At Keyboard
BBL=Be Back Later
BBS=Be Back Soon
BFN=Bye For Now
B4N=Bye For Now
BRB=Be Right Back
BRT=Be Right There
BTW=By The Way
B4=Before
B4N=Bye For Now
CU=See You
CUL8R=See You Later
CYA=See You
FAQ=Frequently Asked Questions
FC=Fingers Crossed
FWIW=For What It's Worth
FYI=For Your Information
GAL=Get A Life
GG=Good Game
GN=Good Night
GMTA=Great Minds Think Alike
GR8=Great!
G9=Genius
IC=I See
ICQ=I Seek you (also a chat program)
ILU=ILU: I Love You
IMHO=In My Honest Opinion
IMO=In My Opinion
IOW=In Other Words
IRL=In Real Life
KISS=Keep It Simple, Stupid
LDR=Long Distance Relationship
LMAO=Laugh My A.. Off
LOL=Laughing Out Loud
LTNS=Long Time No See
L8R=Later
MTE=My Thoughts Exactly
M8=Mate
NRN=No Reply Necessary
OIC=Oh I See
PITA=Pain In The A..
PRT=Party
SFW=Safe for work
TY=Thank you
TMB=Tweet me back
BRB=Be Right Back
IMO=In My Opinion
RLRT=Real-life re-tweet, a close cousin to OH
OOMF=One of my friends/followers
NTS=Note to self
RTFM=Read the f—ing manual
SNAFU=Situation normal, all f—ed up (slang from the US Military)
RLRT=Real-life re-tweet, a close cousin to OH
SMH=Shaking my head
STFW=Search the f—ing web!
TFTT=Thanks for this tweet
SOB=Son of a B—-
TFTF=Thanks for the follow
PRW=Parents Are Watching
ROFL=Rolling On The Floor Laughing
ROFLOL=Rolling On The Floor Laughing Out Loud
ROTFLMAO=Rolling On The Floor Laughing My A.. Off
SK8=Skate
STATS=Your sex and age
ASL=Age, Sex, Location
THX=Thank You
TTFN=Ta-Ta For Now!
TTYL=Talk To You Later
U=You
U2=You Too
U4E=Yours For Ever
WB=Welcome Back
WTF=What The F...
WTG=Way To Go!
WUF=Where Are You From?
W8=Wait...
7K=Sick:-D Laugher
"""
# Thanks : https://github.com/NeelShah18/emot/blob/master/emot/emo_unicode.py
EMOTICONS = {
    u":‑\)": "Happy face or smiley",
    u":\)": "Happy face or smiley",
    u":-\]": "Happy face or smiley",
    u":\]": "Happy face or smiley",
    u":-3": "Happy face smiley",
    u":3": "Happy face smiley",
    u":->": "Happy face smiley",
    u":>": "Happy face smiley",
    u"8-\)": "Happy face smiley",
    u":o\)": "Happy face smiley",
    u":-\}": "Happy face smiley",
    u":\}": "Happy face smiley",
    u":-\)": "Happy face smiley",
    u":c\)": "Happy face smiley",
    u":\^\)": "Happy face smiley",
    u"=\]": "Happy face smiley",
    u"=\)": "Happy face smiley",
    u":‑D": "Laughing, big grin or laugh with glasses",
    u":D": "Laughing, big grin or laugh with glasses",
    u"8‑D": "Laughing, big grin or laugh with glasses",
    u"8D": "Laughing, big grin or laugh with glasses",
    u"X‑D": "Laughing, big grin or laugh with glasses",
    u"XD": "Laughing, big grin or laugh with glasses",
    u"=D": "Laughing, big grin or laugh with glasses",
    u"=3": "Laughing, big grin or laugh with glasses",
    u"B\^D": "Laughing, big grin or laugh with glasses",
    u":-\)\)": "Very happy",
    u":‑\(": "Frown, sad, andry or pouting",
    u":-\(": "Frown, sad, andry or pouting",
    u":\(": "Frown, sad, andry or pouting",
    u":‑c": "Frown, sad, andry or pouting",
    u":c": "Frown, sad, andry or pouting",
    u":‑<": "Frown, sad, andry or pouting",
    u":<": "Frown, sad, andry or pouting",
    u":‑\[": "Frown, sad, andry or pouting",
    u":\[": "Frown, sad, andry or pouting",
    u":-\|\|": "Frown, sad, andry or pouting",
    u">:\[": "Frown, sad, andry or pouting",
    u":\{": "Frown, sad, andry or pouting",
    u":@": "Frown, sad, andry or pouting",
    u">:\(": "Frown, sad, andry or pouting",
    u":'‑\(": "Crying",
    u":'\(": "Crying",
    u":'‑\)": "Tears of happiness",
    u":'\)": "Tears of happiness",
    u"D‑':": "Horror",
    u"D:<": "Disgust",
    u"D:": "Sadness",
    u"D8": "Great dismay",
    u"D;": "Great dismay",
    u"D=": "Great dismay",
    u"DX": "Great dismay",
    u":‑O": "Surprise",
    u":O": "Surprise",
    u":‑o": "Surprise",
    u":o": "Surprise",
    u":-0": "Shock",
    u"8‑0": "Yawn",
    u">:O": "Yawn",
    u":-\*": "Kiss",
    u":\*": "Kiss",
    u":X": "Kiss",
    u";‑\)": "Wink or smirk",
    u";\)": "Wink or smirk",
    u"\*-\)": "Wink or smirk",
    u"\*\)": "Wink or smirk",
    u";‑\]": "Wink or smirk",
    u";\]": "Wink or smirk",
    u";\^\)": "Wink or smirk",
    u":‑,": "Wink or smirk",
    u";D": "Wink or smirk",
    u":‑P": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":P": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"X‑P": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"XP": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":‑Þ": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":Þ": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":b": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"d:": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"=p": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u">:P": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u":‑/": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u":/": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u":-[.]": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u">:[(\\\)]": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u">:/": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u":[(\\\)]": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u"=/": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u"=[(\\\)]": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u":L": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u"=L": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u":S": "Skeptical, annoyed, undecided, uneasy or hesitant",
    u":‑\|": "Straight face",
    u":\|": "Straight face",
    u":$": "Embarrassed or blushing",
    u":‑x": "Sealed lips or wearing braces or tongue-tied",
    u":x": "Sealed lips or wearing braces or tongue-tied",
    u":‑#": "Sealed lips or wearing braces or tongue-tied",
    u":#": "Sealed lips or wearing braces or tongue-tied",
    u":‑&": "Sealed lips or wearing braces or tongue-tied",
    u":&": "Sealed lips or wearing braces or tongue-tied",
    u"O:‑\)": "Angel, saint or innocent",
    u"O:\)": "Angel, saint or innocent",
    u"0:‑3": "Angel, saint or innocent",
    u"0:3": "Angel, saint or innocent",
    u"0:‑\)": "Angel, saint or innocent",
    u"0:\)": "Angel, saint or innocent",
    u":‑b": "Tongue sticking out, cheeky, playful or blowing a raspberry",
    u"0;\^\)": "Angel, saint or innocent",
    u">:‑\)": "Evil or devilish",
    u">:\)": "Evil or devilish",
    u"\}:‑\)": "Evil or devilish",
    u"\}:\)": "Evil or devilish",
    u"3:‑\)": "Evil or devilish",
    u"3:\)": "Evil or devilish",
    u">;\)": "Evil or devilish",
    u"\|;‑\)": "Cool",
    u"\|‑O": "Bored",
    u":‑J": "Tongue-in-cheek",
    u"#‑\)": "Party all night",
    u"%‑\)": "Drunk or confused",
    u"%\)": "Drunk or confused",
    u":-###..": "Being sick",
    u":###..": "Being sick",
    u"<:‑\|": "Dump",
    u"\(>_<\)": "Troubled",
    u"\(>_<\)>": "Troubled",
    u"\(';'\)": "Baby",
    u"\(\^\^>``": "Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"\(\^_\^;\)": "Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"\(-_-;\)": "Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"\(~_~;\) \(・\.・;\)": "Nervous or Embarrassed or Troubled or Shy or Sweat drop",
    u"\(-_-\)zzz": "Sleeping",
    u"\(\^_-\)": "Wink",
    u"\(\(\+_\+\)\)": "Confused",
    u"\(\+o\+\)": "Confused",
    u"\(o\|o\)": "Ultraman",
    u"\^_\^": "Joyful",
    u"\(\^_\^\)/": "Joyful",
    u"\(\^O\^\)／": "Joyful",
    u"\(\^o\^\)／": "Joyful",
    u"\(__\)": "Kowtow as a sign of respect, or dogeza for apology",
    u"_\(\._\.\)_": "Kowtow as a sign of respect, or dogeza for apology",
    u"<\(_ _\)>": "Kowtow as a sign of respect, or dogeza for apology",
    u"<m\(__\)m>": "Kowtow as a sign of respect, or dogeza for apology",
    u"m\(__\)m": "Kowtow as a sign of respect, or dogeza for apology",
    u"m\(_ _\)m": "Kowtow as a sign of respect, or dogeza for apology",
    u"\('_'\)": "Sad or Crying",
    u"\(/_;\)": "Sad or Crying",
    u"\(T_T\) \(;_;\)": "Sad or Crying",
    u"\(;_;": "Sad of Crying",
    u"\(;_:\)": "Sad or Crying",
    u"\(;O;\)": "Sad or Crying",
    u"\(:_;\)": "Sad or Crying",
    u"\(ToT\)": "Sad or Crying",
    u";_;": "Sad or Crying",
    u";-;": "Sad or Crying",
    u";n;": "Sad or Crying",
    u";;": "Sad or Crying",
    u"Q\.Q": "Sad or Crying",
    u"T\.T": "Sad or Crying",
    u"QQ": "Sad or Crying",
    u"Q_Q": "Sad or Crying",
    u"\(-\.-\)": "Shame",
    u"\(-_-\)": "Shame",
    u"\(一一\)": "Shame",
    u"\(；一_一\)": "Shame",
    u"\(=_=\)": "Tired",
    u"\(=\^\·\^=\)": "cat",
    u"\(=\^\·\·\^=\)": "cat",
    u"=_\^=	": "cat",
    u"\(\.\.\)": "Looking down",
    u"\(\._\.\)": "Looking down",
    u"\^m\^": "Giggling with hand covering mouth",
    u"\(\・\・?": "Confusion",
    u"\(?_?\)": "Confusion",
    u">\^_\^<": "Normal Laugh",
    u"<\^!\^>": "Normal Laugh",
    u"\^/\^": "Normal Laugh",
    u"\（\*\^_\^\*）": "Normal Laugh",
    u"\(\^<\^\) \(\^\.\^\)": "Normal Laugh",
    u"\(^\^\)": "Normal Laugh",
    u"\(\^\.\^\)": "Normal Laugh",
    u"\(\^_\^\.\)": "Normal Laugh",
    u"\(\^_\^\)": "Normal Laugh",
    u"\(\^\^\)": "Normal Laugh",
    u"\(\^J\^\)": "Normal Laugh",
    u"\(\*\^\.\^\*\)": "Normal Laugh",
    u"\(\^—\^\）": "Normal Laugh",
    u"\(#\^\.\^#\)": "Normal Laugh",
    u"\（\^—\^\）": "Waving",
    u"\(;_;\)/~~~": "Waving",
    u"\(\^\.\^\)/~~~": "Waving",
    u"\(-_-\)/~~~ \($\·\·\)/~~~": "Waving",
    u"\(T_T\)/~~~": "Waving",
    u"\(ToT\)/~~~": "Waving",
    u"\(\*\^0\^\*\)": "Excited",
    u"\(\*_\*\)": "Amazed",
    u"\(\*_\*;": "Amazed",
    u"\(\+_\+\) \(@_@\)": "Amazed",
    u"\(\*\^\^\)v": "Laughing,Cheerful",
    u"\(\^_\^\)v": "Laughing,Cheerful",
    u"\(\(d[-_-]b\)\)": "Headphones,Listening to music",
    u'\(-"-\)': "Worried",
    u"\(ーー;\)": "Worried",
    u"\(\^0_0\^\)": "Eyeglasses",
    u"\(\＾ｖ\＾\)": "Happy",
    u"\(\＾ｕ\＾\)": "Happy",
    u"\(\^\)o\(\^\)": "Happy",
    u"\(\^O\^\)": "Happy",
    u"\(\^o\^\)": "Happy",
    u"\)\^o\^\(": "Happy",
    u":O o_O": "Surprised",
    u"o_0": "Surprised",
    u"o\.O": "Surpised",
    u"\(o\.o\)": "Surprised",
    u"oO": "Surprised",
    u"\(\*￣m￣\)": "Dissatisfied",
    u"\(‘A`\)": "Snubbed or Deflated"
}
STOPWORDS = set(stopwords.words('english'))
PUNCT_TO_REMOVE = string.punctuation

# Loading data from mongoDB
ca = certifi.where()

client = MongoClient(f"mongodb+srv://{LOGIN}:{PASS}@cluster0.psdqkii.mongodb.net/Twitter", tlsCAFile=ca)
db = client["Ukraine_war"]
collection = db["Putin"]
# Text preprocessing function

lemmatizer = WordNetLemmatizer()

query = {}
cursor = collection.find(query)
df = pd.DataFrame(list(cursor))
# Drop duplicates by id to only get different text data
df.drop_duplicates(subset=["id"], inplace=True)
df.drop_duplicates(subset=["text"], inplace=True)

chat_words_map_dict = {}
chat_words_list = []
spell = SpellChecker()

for line in chat_words_str.split("\n"):
    if line != "":
        cw = line.split("=")[0]
        cw_expanded = line.split("=")[1]
        chat_words_list.append(cw)
        chat_words_map_dict[cw] = cw_expanded
chat_words_list = set(chat_words_list)


def remove_stopwords(text):
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])


def convert_emoticons(text):
    for emot in EMOTICONS:
        text = re.sub(u'(' + emot + ')', "_".join(EMOTICONS[emot].replace(",", "").split()), text)
    return text


def remove_punctation(text):
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))


def chat_words_conversion(text):
    new_text = []
    for w in text:
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return new_text


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)


def lemmatize_words(text):
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])


stop_words = stopwords.words('english')
stemmer = SnowballStemmer('english')

text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z]+"
tweet_tokenizer = TweetTokenizer()


def preprocess(text, stem=False):
    text = " ".join(chat_words_conversion(tweet_tokenizer.tokenize(text)))
    text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(lemmatizer.lemmatize(token))
            else:
                tokens.append(token)
    if "n" in tokens:
        print(tokens)
    return " ".join(tokens)


df["preprocessed_text"] = df["text"].apply(lambda x: preprocess(x))
