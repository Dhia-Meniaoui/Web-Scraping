# packages
from ast import If
from email import header
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json 
import datetime 





class CommercialSales(scrapy.Spider):
    name ='immowelt'
    base_url = 'https://www.immowelt.de/liste/'
    nb_pages = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }


    # constructor init
    def __init__(self):
        # init conent
        content = ''
     # read postcodes file
        with open('german_cities.csv', 'r') as f:
          for line in f.read ():
                content += line
        self.cities = list(filter(None , content.split('\n'))) 
        print (self.cities)


    # general crawler
    def start_requests(self):
        # init filename
        filename = './output/Commercial_Sale_' + datetime.datetime.today().strftime('%Y-%m-%d-%H-%M') + '.jsonl'
        # postcodes count
        
        # loop over postcodes
        for city in self.cities:
            for count in range(1,3):
                next_city= self.base_url+ city + '/haeuser/kaufen?d=true&sd=DESC&sf=RELEVANCE&sp='+ str(count)
                print('sdf')
                print(next_city)
                print(city)
                yield scrapy.Request(url=next_city, headers = self.headers, meta={'city':city ,'filename': filename, 'count': count}, callback = self.parse_links)
                
            
    

    # parse links
    def parse_links(self, res):
        
        # extract forwarded data
        city = res.meta.get('city')
        filename = res.meta.get('filename')   
        count = res.meta.get('count')
  
        # loop over property cards
        for card in res.css('div[class="EstateItem-1c115"]'):
            card_link = card.css('a[class="mainSection-b22fb noProject-eaed4"]::attr(href)').get()
            yield scrapy.Request(url=card_link, headers = self.headers, meta={'city':city ,'filename': filename, 'count': count}, callback = self.parse_listing)
            print(card_link)
                                         
                                         
    # parse listing
    def parse_listing (self, res):

        # extract forwarded data
        #city = res.meta.get('city')
        #filename = res.meta.get('filename')

        content = res.css('strong[class="ng-star-inserted"] *::text').getall()
        print(content)
   
  
        #print(res)

        # extract features
        features = {
                #'id': '',
                #'url': res.url,
                #'city': city,
                'title': res.css('h1[class="ng-star-inserted"] *::text')
                            .getall(),
                'address': '',
                'price': '',
                'agent_name': '',

                'key_features': [],
                'full_description': [],
                'coordinates': {
                    'latitude': '',
                    'longitude': ''
                }
        }
        #print(json.dumps(features ,indent=2))

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CommercialSales)
    process.start()
    
