import string
import math
import re
import sqlite3
import nltk

from nltk.corpus import stopwords

# Connect to sqlite database to store relevancy of words
conn = sqlite3.connect("relevance.db")
c = conn.cursor()

# regex to determine if a word is a username to filter out
user_pattern = re.compile("@(\w+)")

url_pattern = re.compile('https?://[^\s<>"]+|www\.[^\s<>"]+')

# regex to match only alphanumeric characters
alphanumeric_pattern = re.compile("\W+")

def create_relevance_table():
    c.execute('''CREATE TABLE IF NOT EXISTS relevance(word varchar(255) NOT NULL, occ int, rocc int, irocc int, PRIMARY KEY (word));''')
    conn.commit()

# Removes stopwords, punctuation and usernames
# returns list of the original tweet and the list of filtered words
def remove_chaff(tweet):
    tweet_text = tweet[0].lower()

    # Split tweet body into list of strings
    tweet_word_list = tweet_text.split()
    
    filtered_words = []

    # Filter the word list to only words that aren't stopwords or usernames
    # and strip out non-alphanumeric characters
    for word in tweet_word_list:
        if not user_pattern.match(word) and not url_pattern.match(word):
            stripped_word = alphanumeric_pattern.sub('', word)
            if stripped_word not in stopwords.words('english') and stripped_word != 'rt':
                filtered_words += [stripped_word]

    # Remove duplicate words
    filtered_words = list(set(filtered_words))

    return filtered_words


# Updates the occurence counter for each word in a word list in the relevance
# database, adds that word if it doesn't exist
def tweet_to_relevance_table(tweet):
    create_relevance_table()
    word_list = remove_chaff(tweet)
    for word in word_list:
        c.execute('''INSERT OR IGNORE INTO relevance(word, occ, rocc, irocc) VALUES("''' + word + '''", 0, 0, 0);''')
        #c.execute('''UPDATE relevance SET occ = occ + 1 WHERE word = "''' + word + '''";''')

    conn.commit()

# Update the relevancy occurence counters in relevancy database given a list
# of words
def update_relevancy(tweet, relevant):
    word_list = remove_chaff(tweet)
    if relevant:
        for word in word_list:
             c.execute('''UPDATE relevance SET rocc = rocc + 1, occ = occ + 1 WHERE word = "''' + word + '''";''')
    else:
        for word in word_list:
             c.execute('''UPDATE relevance SET irocc = irocc + 1, occ = occ + 1 WHERE word = "''' + word + '''";''')    
    conn.commit()



# Calculates the relevancy of a tweet using the Bayesian filtering method, with
# probability of relevance
def tweet_relevancy(tweet):
    word_list = remove_chaff(tweet)

    # Return middle value if word list empty
    if word_list == []: return 0.5

    relevancies = fetch_word_relevancies(word_list)

    tmpprob1 = 1
    tmpprob2 = 1
    
    for relevance in relevancies:
        if relevance[1] != 0 or relevance[2] !=0:
            p = (relevance[1]/float(relevance[0])) / ((relevance[2]/float(relevance[0])) + (relevance[1]/float(relevance[0])))
            tmpprob1 *= p
            tmpprob2 *= (1 - p)
    
    if tmpprob1 + tmpprob2 == 0: return 0.5
    return tmpprob1/(tmpprob1+tmpprob2)


def fetch_word_relevancies(word_list):
    relevancies = []
    for word in word_list:
        c.execute('''SELECT occ, rocc, irocc FROM relevance WHERE word = "''' + word + '''";''')
        relevancies += [c.fetchone()]
    return relevancies



## TESTING
def test_tweet():
    fo = open("crash2.csv", "r")
    tweets = []
    for line in fo:
        line_list = line.split(",")
        del line_list[0]
        
        tweet_to_relevance_table(line_list)

        tweets += [line_list]

    for tweet in tweets:
        print(tweet[0])
        com = raw_input();
        if com == "y":
            update_relevancy(tweet, True)
        else:
            update_relevancy(tweet, False)

def test_sort():
    fo = open("crash.csv", "r")
    tweets = []
    for line in fo:
        line_list = line.split(",")
        del line_list[0]
        
        tweet_to_relevance_table(line_list)

        tweets += [line_list]

    tweetrels = []
    for tweet in tweets:
        rel = tweet_relevancy(tweet)
        tweetrels += [rel, tweet[0]]

    print tweetrels
