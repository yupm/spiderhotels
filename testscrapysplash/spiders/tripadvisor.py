import scrapy
from scrapy import Selector
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest

#This function can extract all the singaopre hotel url on the current page, press the next button, and continue until end of hotel 

MAIN_URL = 'https://www.tripadvisor.com.sg'

class TravelSpider (scrapy.Spider):
        name = "tripadvisor"
        
        start_urls = [
            'https://www.tripadvisor.com.sg/Hotels-g294265-oa30-Singapore-Hotels.html',
        ]
        
        def parse(self, response):        
            #enter hotel page
            hotels =  response.css('div.listing_title a.property_title.prominent::attr("href")')
            for hotel in hotels:
                yield response.follow(hotel.extract(), self.parse_hotel_reviews)
            
            next_page = response.css('div.unified.ui_pagination a.primary::attr("href")').extract_first()
            
            if next_page is not None:
                yield response.follow(next_page, self.parse)                             
            else:
                inspect_response(response, self)

        def parse_hotel_reviews(self, response):
            print("Checking hotel ", response.url)
            