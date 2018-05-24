from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sqlite3 as sql
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

conn = sql.connect('twitter_sentiment.db')
cursor = conn.cursor()

consumer_key = "JfhNSUpRBnCkQekjkTOIL86uR"
consumer_secret = "StOVv2LE3HASVAp1pPP3sZkbucEXnPLMssVAcxPsQ3F7POAaxA"
access_token = "444822244-BnyUlvHCrRJ0gB7LLgZOuH96aSfMrL9f8Mi8mXRT"
access_secret = "EWpuLcNJ3WcNCmBQ17b1CBwPtAviBQyb0jgI9KGdZvsiU"

def create_table():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        cursor.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        cursor.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        cursor.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(f"Database Error: {str(e)}")

create_table()

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            cursor.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                  (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(f"Status error: {status}")

while True:
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track = ["a","e","i","o","u"])
    except Exception as e:
        print(f"Error: {str(e)}")
        time.sleep(5)
