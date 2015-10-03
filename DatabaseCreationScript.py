import sqlite3

#Create database named date
data = sqlite3.connect('hackathon_starter/db.sqlite3')
c=data.cursor()

#Create table for tweet data
c.execute('''CREATE TABLE hackathon_tweet (body text, postcode text, latitude real, longitude real, url text UNIQUE, event integer, time numeric, relevance real);''')

#Create table for event data
c.execute('''CREATE TABLE  hackathon_event (id integer, postcode text, event text, time numeric, occurances integer);''')

data.close()
