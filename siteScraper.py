from lxml import html
import requests
import HTMLParser
from stripogram import html2text
import pickle
places = {}

def singlePageScrape(no):
    global places
    h = HTMLParser.HTMLParser()
    page = requests.get('https://www.list.co.uk/places/location:Glasgow(55.8621,-4.2465)/distance:10/page:' + no + "/#results'")
    tree = html.fromstring(page.text)
    buyers = tree.xpath('//h2[@class="head"]/text()')
    prices = tree.xpath('//span[@class="postal-code"]/text()')
    count = 0
    for item in buyers:
        places[str(item.encode('ascii','ignore'))] = str(html2text(prices[count]).encode('ascii','ignore'))
        count += 1

def multiScrape():  ##Returns dictionary, places, {University of Glasgow:G234HJ,Place:postcode}
    no = 1
    while no < 41:
        singlePageScrape(str(no))
        no += 1
    return places

f = open('locations','a')
places = multiScrape()
placesList = []
for item in places:
    f.write(str(item.encode('ascii','ignore'))+'\n')
    f.write(str(places[item].encode('ascii','ignore'))+'\n')


f.close()
