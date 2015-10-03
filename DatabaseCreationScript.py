import sqlite3

#Create database named date
data = sqlite3.connect('data.db')
c=data.cursor()

#Create table for tweet data
c.execute('''CREATE TABLE Tweet (postcode text, body text, time text, event text)''')

#Create table for event data
c.execute('''CREATE TABLE  Event (postcode text, event text, occurances integer)''')

data.close()
