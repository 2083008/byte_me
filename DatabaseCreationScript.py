import sqlite3

#Create database named date
data = sqlite3.connect('data.db')
c=data.cursor()

#Create table for tweet data
c.execute('''CREATE TABLE Tweet (body text, postcode text, latitude float, longitude float, url text UNIQUE, event integer, time datetime, relevance float);''')

#Create table for event data
c.execute('''CREATE TABLE  Event (id integer, postcode text, event text, time datetime, occurances integer);''')

data.close()
