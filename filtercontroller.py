import tweetfilter as tf
import sqlite3
import tagTweetsToEvents as ttte

conn = sqlite3.connect("hackathon_starter/db.sqlite3")
c = conn.cursor()

def update_all_relevancies():
    upconn = sqlite3.connect("hackathon_starter/db.sqlite3")
    uc = upconn.cursor()
    uc.execute('''SELECT body, url FROM hackathon_tweet''')
    tweets = uc.fetchall()
    for tweet in tweets:
        tr = tf.tweet_relevancy(tweet)
        uc.execute('''UPDATE hackathon_tweet SET relevancy = ? WHERE url = ?;''', tr, tweet[1])
        
    upconn.commit()
    upconn.close()

def add_tweet(tweet):
    tf.tweet_to_relevance_table(tweet)
    tr = tf.tweet_relevancy(tweet)
    ttte.checkEvents(tweet[3], tweet[0], tweet[2], tweet[1][1], tweet[1][0], tr, tweet[4])
    

def mark_irrelevant(tweet_url):
    c.execute('''SELECT body, url FROM hackathon_tweet WHERE url = ?''', tweet_url)
    tweet = c.fetchone()
    tf.update_relevancy(tweet, false)
    update_all_relevancies()

def mark_relevant(tweet_url):
    c.execute('''SELECT body, url FROM hackathon_tweet WHERE url = ?''', tweet_url)
    tweet = c.fetchone()
    tf.update_relevancy(tweet, true)
    update_all_relevancies()
