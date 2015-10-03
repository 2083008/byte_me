from lxml import html
import requests

def singlePageScrape(no):
    global places
    page = requests.get('https://www.list.co.uk/places/location:Glasgow(55.8621,-4.2465)/distance:10/page:' + no + "/#results'")
    tree = html.fromstring(page.text)
    buyers = tree.xpath('//h2[@class="head"]/text()')
    prices = tree.xpath('//span[@class="postal-code"]/text()')
    x = 0
    for item in buyers:
        places += [item,prices[x].encode('ascii','ignore')]
        x+=1
        
places =[]
no = 1
while no < 41:
    singlePageScrape(str(no))
    no += 1


print places
        


