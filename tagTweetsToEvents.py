#Within the checkTweets and checkEvents functions a more thorough check should be carried out involving the amount of similarities and therefore chance of being identical

import sqlite3
import math
import difflib

data = sqlite3.connect('data.db')
c=data.cursor()

#Remove the redundant linking words of a tweet
def splitTweet(tweet):
    redundantWords = ['and', 'in', 'addition', 'as', 'well', 'as', 'the', 'my','who','do',
                        'also', 'aoo', 'furthermore', 'moreover', 'of', 'is','be','you','that'
                        'apart', 'from', 'so', 'to', 'besides', 'a', 'I', 'am','are','like'
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
                        score += 7
                    else:
                        score += containsForHashTags(word[1:].lower(),word2[1:].lower())
    return score

def checkLocation(location1,location2):
    score = 0
    if location1 == location2:
        score += 5
    else:
        if (int(location2[1:]) - int(location1[1:])) <2 or (int(location2[1:])-int(location1[1:]) < 2):
            score += 3
    return score

def checkTime(time1,time2):
    time1 = time1
    time2 = time2
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
                score+=6
            if contains(word.lower(),word2.lower()):
                score +=4
    return score


#check new tweet against the database of tweets to see if it is trending
def checkTweets(location,tweetBody,time):
    tweet = splitTweet(tweetBody)
    #Get all tweets from the database
    c.execute("SELECT body from Tweet")
    allTweets = c.fetchall()
    #Get all locations from database
    c.execute("SELECT postcode from Tweet")
    allPostcodes = c.fetchall()
    #Get all times from database
    c.execute("SELECT time from Tweet")
    allTimes = c.fetchall()

    
    mostRelatedScore =0
    mostRelatedTweet =''
    tweetToEvent = ''
    #Loop through i times where i is the number of entries
    for i in range(0,len(allTweets)):
        c.execute("SELECT event from Tweet WHERE body = (?)",(allTweets[i]))
        tweetEvent = c.fetchone()
        if tweetEvent[0] == '':
            oldTweet = splitTweet(allTweets[i][0])
            for string in oldTweet:
                score = areRelated(string,tweetBody)
                score += checkHashTags(string,tweetBody)
                score += checkLocation(location,allPostcodes[i][0])
                score += checkTime(time,allTimes[i][0])
                if score>5 and score>mostRelatedScore:
                    mostRelatedScore = score
                    mostRelatedTweet = allTweets[i][0]
            if mostRelatedTweet != '':
                c.execute("INSERT INTO Event VALUES(?,?,?,?)",(location,mostRelatedTweet,time,2))
                c.execute("UPDATE Tweet SET event = (?) WHERE body = (?)",(mostRelatedTweet,mostRelatedTweet))
                c.execute("INSERT INTO Tweet VALUES(?,?,?,?)",(location,tweetBody,time,mostRelatedTweet))
                data.commit()
                return
    c.execute("INSERT INTO Tweet VALUES(?,?,?,?)",(location,tweetBody,time,''))
    data.commit()
        
                    

#check new tweet against the database of events to see if it already exists in events
def checkEvents(location,tweetBody,time):
    tweet = splitTweet(tweetBody)
    #collect all of the events from the database
    c.execute("SELECT event from Event")
    events = c.fetchall()
    #Get all locations from the database
    c.execute("SELECT postcode from Event")
    locations = c.fetchall()
    c.execute("SELECT time from Event")
    times = c.fetchall()
    
    mostRelatedScore = 0
    mostRelatedString = ''
    for i in range(0,len(events)):
        string = events[i][0]
        score = areRelated(string,tweetBody)
        score += checkHashTags(string,tweetBody)
        score += checkLocation(location,locations[i][0])
        score += checkTime(time,times[i][0])
        if score>5 and score>mostRelatedScore:
            mostRelatedScore = score
            mostRelatedString = string

    if mostRelatedString !='':
        c.execute("UPDATE Event SET occurances = occurances + 1 WHERE event = ?", (mostRelatedString,))
        c.execute("INSERT INTO Tweet VALUES(?,?,?,?)",(location,tweetBody,time,mostRelatedString))
        data.commit()
    else:
        checkTweets(location,tweetBody,time)

test_file =open('exampleTweets.txt', 'r')
n=0
while n < 20:
    tweetLocation = test_file.readline()[:-1]
    tweetBody = test_file.readline()[:-1]
    tweetTime= test_file.readline()[:-1]
    checkEvents(tweetLocation,tweetBody,tweetTime)
    n+=1


    
