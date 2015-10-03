import tweetfilter as tf
import sqlite3
import tagTweetsToEvents as ttte

conn = sqlite3.connect("data.db")
c = conn.cursor()

def update_all_relevancies():
    c.execute('''SELECT * FROM Tweet''')
    tweets = c.fetchall()
    for tweet in tweets:
        tr = tweet_relevancy(tweet)
        c.execute('''UPDATE Tweet SET relevance = ''', tr, ''' WHERE url = ''', tweet[4], ''';''')


def add_tweet(tweet):
    tf.tweet_to_relevance_table(tweet)
    tr = tweet_relevancy(tweet)
    ttte.checkTweets(tweet[3], tweet[0], tweet[2], tweet[1][1], tweet[1][0], tr, tweet[4])
    
