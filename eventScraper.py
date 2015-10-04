from TwitterAPI import TwitterAPI
import googlemaps
from math import *
from lxml import html
import urllib2
import HTMLParser
import requests
import difflib
import nltk   
from urllib import urlopen
from stripogram import html2text
places = {}

no = str(1)
def singlePageScrape(no):
    global places
    response = urllib2.urlopen('''https://www.list.co.uk/events/location:Glasgow(55.8621,-4.2465)/distance:10/sort:date/page:''' + no + '''/#results''')
    page_source = response.read()
    x = 0
    while (x+2 < len(page_source)):
        found = False
        if (page_source[x] == '<' and page_source[x+1] == 's' and page_source[x+2] == 'p'):
            start = x
            x = x+1
            while found == False:
                if (page_source[x] == '<' and page_source[x+1] == '/' and page_source[x+2] == 's'):
                    end = x
                    line = page_source[start:end]
                    found = True
                    x+=1
                    haystack = line
                    if haystack.find("title") >= 0:
                        titleOn = haystack[haystack.find("title"):]
                        haystack = titleOn
                        if haystack.find(',') >= 0:
                            eventTitle = haystack[7:haystack.find(',')]
                            haystack = eventTitle
                            if haystack.find(':') >= 0:
                                eventTitle = eventTitle[:haystack.find(':')]
                            print eventTitle
                    else:
                        continue

                else:
                    x=x+1
        else:
            x+=1
                
                


singlePageScrape(no)
print places
