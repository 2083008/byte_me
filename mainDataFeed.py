from TwitterAPI import TwitterAPI
import googlemaps
from math import *
from lxml import html
import HTMLParser
import requests
import difflib
import nltk   
from urllib import urlopen
from stripogram import html2text
api = TwitterAPI("jt9lHyz5rkanAMG7Z4AQKTEg5", 
                 "xpw3BqaIO45jMMSQSyDRuYSzKTvOkevoTwUB7iDIaT7p4xVZru", 
                 "131952295-lgmR5htQiEBN9dsbjQ9xoZj5rn0eLdqIFMf0ap97", 
                 "iGm1CY0eOnlDjohmj7iBLYz52cp0nYuSCn4lukjo6NrzP")
split = []
places = {}
placesData = {}
placeMentionned = ''
officerGPS = {}
officerGPS['Bob'] = [55.95708137,-4.09057387]
officerGPS['John'] = [55.80673623,-4.42363939]
officerGPS['Paul'] = [55.80527978,-4.0248262]
officerGPS['Tom'] = [55.89574027,-4.22762588]
officerGPS['Mike'] = [55.77021703,-4.06350479]
officerGPS['Allan'] = [55.87150646,-4.42722515]


def singlePageScrape(no):
    global places
    h = HTMLParser.HTMLParser()
    page = requests.get('https://www.list.co.uk/places/location:Glasgow(55.8621,-4.2465)/distance:10/page:' + no + "/#results'")
    tree = html.fromstring(page.text)
    buyers = tree.xpath('//h2[@class="head"]/text()')
    prices = tree.xpath('//span[@class="postal-code"]/text()')
    count = 0
    for item in buyers:
        places[item] = html2text(prices[count]).encode('ascii','ignore')
        count += 1

def multiScrape():  ##Returns dictionary, places, {University of Glasgow:G234HJ,Place:postcode}
    no = 1
    while no < 41:
        singlePageScrape(str(no))
        no += 1
    return places

def degToRad(deg):
    return deg * pi / 180

def radToDeg(rad):
    return rad * 180 /pi

def boxToCentre(coords):
    a = []
    b = []
    c = []
    n = len(coords)
    for item in coords:
        a += [cos(degToRad(item[0])) * cos(degToRad(item[1]))]
        b += [cos(degToRad(item[0])) * sin(degToRad(item[1]))]
        c += [sin(degToRad(item[0]))]
    x = (a[0] + a[1] + a[2] + a[3]) / n
    y = (b[0] + b[1] + b[2] + b[3]) / n
    z = (c[0] + c[1] + c[2] + c[3]) / n
    lonFinal = atan2(y, x)
    hyp = sqrt(x * x + y * y)
    latFinal = atan2(z, hyp)
    return [radToDeg(lonFinal),radToDeg(latFinal)]

def postBoxes():
    global split
    names = '''G1 G2 G3 G4 G5 G9 G11 G12 G13 G14 G15 G20 G21 G22 G23 G31 G32 G33 G34 G40 G41 G42 G43 G44 G45 G46 G51 G52 G53 G58 G60 G61 G62 G63 G64 G65 G66 G67 G68 G69 G70 G71 G72 G73 G74 G75 G76 G77 G78 G79 G81 G82 G83 G84 G90'''
    split = names.split()
    dist_range = 0.74 / 69.172
    coordinateFile = open('postcodes.txt','r')
    coordinates = []
    lister = []
    finalCoords = {}
    x = 0
    for item in coordinateFile:
        lister += [float(item[:-1])]
        if len(lister) == 2:
            coordinates += [lister]
            lister = []
    for item in coordinates:
        lat_range = [item[0]-dist_range, item[0]+dist_range]
        lon_range = [item[1]-dist_range, item[1]+dist_range]
        finalCoords[split[x]] = [lat_range,lon_range]
        x+=1
    return finalCoords
            
def nameToCoords(name):
    gmaps = googlemaps.Client(key='AIzaSyD081cPrBCVqJGvEyEuvRyjtebmN3hw5wI')
    location = name + ", Glasgow, Glasgow City"
    address = gmaps.geocode(name, components={'region': 'GB','locality':'Glasgow'})
    formatted_address = address[0]['formatted_address']
    if formatted_address != 'Glasgow, Glasgow City, UK':
        return [address[0]['geometry']['location']['lat'],address[0]['geometry']['location']['lng']]


def tweetLocationFromText(tweet):
    global placesData
    global placeMentionned
    tweetNoSpace = ''
    for character in tweet:
        if character != ' ':
            tweetNoSpace += character
    simH = 0
    for place in placesData:
        placeNoSpace =''
        for character in place:
            if character != ' ':
                placeNoSpace += character
        l = len(placeNoSpace)
        endChar = l
        position = 0
        while position + endChar < len(tweetNoSpace) + 1:
            sim = difflib.SequenceMatcher(None,tweetNoSpace[position:position + endChar].lower(),placeNoSpace.lower()).ratio()
            position +=1
            if sim > 0.9:
                if sim > simH:
                    placeMentionned = place
    if placeMentionned != '':
        return placesData[placeMentionned]
    else:
        return "abcdefg123"

def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return 0.846541* c * r

def currentEvents():
    global placesData

def mainThread():
    global api
    global placesData
    global placeMentionned
    placesData = multiScrape()
    placesData['University of Glasgow'] ='G12 8QQ'
    placesData['Hackathon'] ='G12 8QQ'
    placesData['Uofg'] ='G12 8QQ'
    placesData['Glasgow uni'] ='G12 8QQ'
    placesData['Boyd Orr'] = 'G12 8QR'
    placesData['The SSE Hydro'] = 'G3 8YW'
    placesData['HiltonHotel'] = 'G3 8HT'
    postCodes = postBoxes()
    dictionary = {}
    pos = 0
    while 1:
        try:
            tweetsFromGlasgow = api.request('statuses/filter', {'locations':'-4.487958,55.759649,-3.992752,55.973084'})
            break
        except:
            continue
    for tweet in tweetsFromGlasgow:
        loc = boxToCentre(tweet["place"]["bounding_box"]["coordinates"][0])
        tweetFull = [tweet["text"].encode('ascii','ignore'),loc,float(tweet["timestamp_ms"])]
        postcodelist = []
        accurate = False
        constructed = False
##        for item in postCodes:
##            lonL = postCodes[item][0][0]
##            lonH = postCodes[item][0][1]
##            latL = postCodes[item][1][0]
##            latH = postCodes[item][1][1]
##            if loc[0] > lonL:
##                if loc[0] < lonH:
##                    if loc[1] > latL:
##                        if loc[1] < latH:
##                            try:
##                                if item not in postcodelist:
##                                    postcodelist += [item]                                
##                                dictionary[item] += [tweetFull]
##                            except:
##                                if item not in postcodelist:
##                                    postcodelist += [item]
##                                dictionary[item] = [tweetFull]
##                                continue
        gmaps = googlemaps.Client(key='AIzaSyD081cPrBCVqJGvEyEuvRyjtebmN3hw5wI')
        reverse_geocode_result = gmaps.reverse_geocode((loc[0],loc[1]))[0]['formatted_address']
        relevant = reverse_geocode_result.split(',')[-2:-1]
        relevantSplit = relevant[0].split()
        mostLikelyPostCode = ''
        relevantSplit
        for item in relevantSplit:
            section = ''
            for character in item:
                if character in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
                    section += character
            if len(section) == len(item):
                mostLikelyPostCode += str(section)
                break
        postcodelist = mostLikelyPostCode
        accLoc = tweetLocationFromText(tweetFull[0])
        if accLoc != "abcdefg123":
            accurate = True
            tweetFull[1] = nameToCoords(accLoc)
            tweetFull += [[accLoc]] + ['https://twitter.com/statuses/'+str(tweet['id_str'].encode('ascii','ignore'))] +[[[accurate],[placeMentionned]]]
            placeMentionned = ''
            constructed = True
        if postcodelist[0][0] == "G":
            if constructed == False:
                accurate = False
                tweetFull = tweetFull + [postcodelist] + ['https://twitter.com/statuses/'+str(tweet['id_str'].encode('ascii','ignore'))] + [[[accurate],['']]]      ## print dictionary
        else:
            continue
        print tweetFull
        print "\n\n\n"
        ## Continue at this indentation to work on current tweet

mainThread()
