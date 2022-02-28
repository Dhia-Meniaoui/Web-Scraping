# packages
from ast import If
from email import header
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import xlsxwriter 
from threading import Timer

class CommercialSales(scrapy.Spider):
    base_url = 'https://www.immowelt.de/liste/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    wb = xlsxwriter.Workbook('datapfe.xlsx')
    ws = wb.add_worksheet('Data')
    ln= 1
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

        
        # loop over postcodes
        for city in self.cities:
            for count in range(1,10):
                next_city= self.base_url+ city + '/haeuser/kaufen?d=true&sd=DESC&sf=RELEVANCE&sp='+ str(count)
                print('sdf')
                print(next_city)
                print(city)
                yield scrapy.Request(url=next_city, headers = self.headers, meta={'city':city , 'count': count}, callback = self.parse_links)
                
           
    

    # parse links
    def parse_links(self, res):
        
        # extract forwarded data
        city = res.meta.get('city')
        count = res.meta.get('count')
        # loop over property cards
        for card in res.css('div[class="EstateItem-1c115"]'):
            card_link = card.css('a[class="mainSection-b22fb noProject-eaed4"]::attr(href)').get()
            yield scrapy.Request(url=card_link, headers = self.headers, meta={'city':city , 'count': count}, callback = self.parse_listing)
            print(card_link)
        
                                         
                                         
    # parse listing
    def parse_listing (self, res):
          
        price = str(res.css('strong[class="ng-star-inserted"] *::text').getall()[0])[:-2]
        surface = str(res.css('span[class="has-font-300"] *::text').getall()[0])
        room = str(res.css('span[class="has-font-300"] *::text').getall()[1])
        self.ws.write(self.ln,1,price) 
        self.ws.write(self.ln,2,surface) 
        self.ws.write(self.ln,3,room)
        self.ln = self.ln +1    
        
        


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CommercialSales)
    process.start()
    CommercialSales.wb.close()
