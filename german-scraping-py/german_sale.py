# packages
from ast import If
from dataclasses import replace
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
            for count in range(1,2):
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
        list1 = res.css('sd-cell-col[class="cell__col"] *::text').getall()
        list2 = res.css('li[class="ng-star-inserted"] *::text').getall()
        price =  str(res.css('strong[class="ng-star-inserted"] *::text').getall()[0])[:-2]
        price = int(price.replace(".",""))
        surface = str(res.css('span[class="has-font-300"] *::text').getall()[0])
        room = str(res.css('span[class="has-font-300"] *::text').getall()[1])
        city = str(res.meta.get('city'))
        address1 = str(res.css('span[class="has-font-100 is-bold flex flex-wrap"] *::text').getall()[0])+str(res.css('span[class="has-font-100 is-bold flex flex-wrap"] *::text').getall()[1])
        state = list2[list2.index('Zustand: ') + 1]
        basement = ("voll unterkellert" in str(list2))
        fitted_kitchen = ("Einbauküche" in str(list2))
        Terrasse = ("Terrasse" in str(list2))
        equipment = ("Ausstattung" in str(list2))
        year = int(list1[list1.index('Baujahr') + 1])
        efficiency_class = str(list1[list1.index('Effizienzklasse') + 1])
        Category = str(list1[list1.index('Kategorie') + 1])
        self.ws.write(self.ln,1,price) 
        self.ws.write(self.ln,2,surface) 
        self.ws.write(self.ln,3,room)
        self.ws.write(self.ln,4,city) 
        self.ws.write(self.ln,5,address1) 
        self.ws.write(self.ln,6,year)
        self.ws.write(self.ln,7,efficiency_class)
        self.ws.write(self.ln,8,Category)
        self.ws.write(self.ln,9,state)
        self.ws.write(self.ln,10,basement)
        self.ws.write(self.ln,11,fitted_kitchen)
        self.ws.write(self.ln,12,Terrasse)
        self.ws.write(self.ln,13,equipment)
        self.ln = self.ln +1    
        
        


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CommercialSales)
    process.start()
    CommercialSales.wb.close()
