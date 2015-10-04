import sqlite3
import math
import difflib
import time

EVENT_ID = 0

data = sqlite3.connect('hackathon_starter/db.sqlite3')
c=data.cursor()

def convertTime(epochTime):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(epochTime))

#Remove the redundant linking words of a tweet
def splitTweet(tweet):
    redundantWords = ['and', 'in', 'addition', 'as', 'well', 'as', 'the', 'my','who','do',
                        'also', 'aoo', 'furthermore', 'moreover', 'of', 'is','be','you','that'
                        'apart', 'from', 'so', 'to', 'besides', 'a', 'I', 'am','are','like',
                      ',','!']
    words = tweet.split()
    for word in words:
        for redundantWord in redundantWords:
            if word == redundantWord:
                words.remove(word)
    return words

def containsForHashTags(word,word2):
    if difflib.SequenceMatcher(None,word,word2).ratio() > 0.3:
        return 6
    return 0


#A function to check if one word contains another word
def contains(word, subword):
    #if the subword is larger than the word then switch them around
    if len(subword)>len(word):
        temp = subword
        subword = word
        word = temp
    isContained = False
    for i in range(0,len(word)-len(subword)):
        if subword[0] == word[i]:
            isContained = True
            for j in range(0,len(subword)):
                if word[i+j] != subword[j]:
                   isContained = False
    return isContained

#checks any hashtags included in tweets and adds to the score
def checkHashTags(string1,string2):
    score = 0
    string1 = string1.split()
    string2=string2.split()
    for word in string1:
        if word[0] == '#':
            for word2 in string2:
                if word2[0] == '#':
                    if word[1:].lower() == word2[1:].lower():
                        score += 15
                    else:
                        score += containsForHashTags(word[1:].lower(),word2[1:].lower())
    return score

def checkLocation(location1,location2):
    score = 0
    if location1 == location2 and (len(location1) >3 or len(location2)>3):
        return 20

    location1 = location1.split()
    location2= location2.split()
    if location1[0] == location2[0]:
        score+=5
    else:
        try:
            if (int(location2[1:]) - int(location1[1:])) <2 or (int(location2[1:])-int(location1[1:]) < 2):
                score +=3
        except:
            return 0
    return score

def checkTime(time1,time2):
    try:
        time1 = int(time1)
        time2 = int(time2)
    except:
        return 0
    if time1-time2 >0:
        difference = time1-time2
    else:
        difference = time2-time1
    if difference == 0 or difference == 1:
        return 10
    return int((1/(math.log(difference,10)))*3)

#Determines if two strings are related and returns a score based on the chance of them being related (0 if unrelated)
def areRelated(string1,string2):
    string1 = string1.split()
    string2=string2.split()
    score = 0
    for word in string1:
        for word2 in string2:
            if word.lower() == word2.lower():
                score+=10
            if contains(word.lower(),word2.lower()):
                score +=6
    return score


#check new tweet against the database of tweets to see if it is trending
def checkTweets(location,tweetBody,epochTime,longitude,latitude,relevancy,url):
    tweet = splitTweet(tweetBody)
    #Get all tweets from the database
    c.execute("SELECT body from hackathon_tweet")
    allTweets = c.fetchall()
    #Get all locations from database
    c.execute("SELECT postcode from hackathon_tweet")
    allPostcodes = c.fetchall()
    #Get all times from database
    c.execute("SELECT time from hackathon_tweet")
    allTimes = c.fetchall()
    
    mostRelatedScore =0
    mostRelatedTweet =''
    tweetToEvent = ''
    #Loop through i times where i is the number of entries
    for i in range(0,len(allTweets)):
        c.execute("SELECT event_id from hackathon_tweet WHERE body = (?)",(allTweets[i]))
        tweetEvent = c.fetchone()
        if tweetEvent[0] == 0:
            oldTweet = splitTweet(allTweets[i][0])
            for string in oldTweet:
                score = areRelated(string,tweetBody)
                score += checkHashTags(string,tweetBody)
                score += checkLocation(location,allPostcodes[i][0])
                score += checkTime(epochTime,allTimes[i][0])
                if score>15 and score>mostRelatedScore:
                    mostRelatedScore = score
                    mostRelatedTweet = allTweets[i][0]
            if mostRelatedTweet != '':
                dateTime = convertTime(epochTime)
                c.execute("INSERT INTO hackathon_event (id,postcode,event,time,occurences)VALUES(NULL,?,?,?,?)",(location,mostRelatedTweet,dateTime,2))
                event_id = c.lastrowid
                c.execute("UPDATE hackathon_tweet SET event_id = (?) WHERE body = (?)",(event_id,mostRelatedTweet))
                c.execute("INSERT INTO hackathon_tweet (postcode,body,time,longitude,latitude,event_id,relevancy,url) VALUES(?,?,?,?,?,?,?,?)",(location,tweetBody,dateTime,longitude,latitude,event_id,relevancy,url))
                data.commit()
                return
    dateTime =convertTime(epochTime)
    c.execute("INSERT INTO hackathon_tweet (postcode,body,time,longitude,latitude,event_id,relevancy,url) VALUES(?,?,?,?,?,?,?,?)",(location,tweetBody,dateTime,longitude,latitude,0,relevancy,url))
    data.commit()
        
                    
#check new tweet against the database of events to see if it already exists in events
def checkEvents(location,tweetBody,epochTime,longitude,latitude, relevancy,url):
    print location
    if type(location) == list:
            location = location[0]
    tweet = splitTweet(tweetBody)
    #collect all of the events from the database
    c.execute("SELECT event from hackathon_event")
    events = c.fetchall()
    #Get all locations from the database
    c.execute("SELECT postcode from hackathon_event")
    locations = c.fetchall()
    c.execute("SELECT time from hackathon_event")
    times = c.fetchall()
    
    mostRelatedScore = 0
    mostRelatedString = ''
    for i in range(0,len(events)):
        string = events[i][0]
        score = areRelated(string,tweetBody)
        score += checkHashTags(string,tweetBody)
        score += checkLocation(location,locations[i][0])
        score += checkTime(epochTime,times[i][0])
        if score>15 and score>mostRelatedScore:
            mostRelatedScore = score
            mostRelatedString = string

    if mostRelatedString !='':
        c.execute("SELECT id from hackathon_event WHERE event = ?",(mostRelatedString,))
        event_id = c.fetchone()
        c.execute("UPDATE hackathon_event SET occurences = occurences + 1 WHERE id = ?",(event_id))
        c.execute("INSERT INTO hackathon_tweet (postcode,body,time,longitude,latitude,event_id,relevancy,url) VALUES(?,?,?,?,?,?,?,?)",(location,tweetBody,convertTime(epochTime),longitude,latitude,event_id[0],relevancy,url))
        data.commit()
    else:
        checkTweets(location,tweetBody,epochTime,longitude,latitude,relevancy,url)

    
