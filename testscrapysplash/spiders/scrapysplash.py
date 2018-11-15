import scrapy
from scrapy_splash import SplashRequest
from scrapy.shell import inspect_response

#error in this program, unable to execute full if else statement in start_requests

class SplashSpider(scrapy.Spider):
    name = "scrapysplash"

    def parse_families(self, response):
        script = """
        function main(splash)
            splash:go(splash.args.url) 
            splash:runjs('document.getElementsByClassName("choices")[1].getElementsByClassName("ui_checkbox item")[0].getElementsByTagName("input")[0].click();') 
            splash:wait(1) 
            return splash:html() 
        end
        """
        yield scrapy.Request(response.url, self.parse_families_reviewers, meta={
            'splash': {
                'args': {'lua_source': script },
                'endpoint': 'execute',
            }
        })

    def parse_couples(self, response):
        script = """
        function main(splash)
            splash:go(splash.args.url) 
            splash:runjs('document.getElementsByClassName("choices")[1].getElementsByClassName("ui_checkbox item")[1].getElementsByTagName("input")[0].click();') 
            splash:wait(1) 
            return splash:html() 
        end
        """
        yield scrapy.Request(response.url, self.parse_couples_reviewers, meta={
            'splash': {
                'args': {'lua_source': script },
                'endpoint': 'execute',
            }
        })
    
    def parse_solo(self, response):
        script = """
        function main(splash)
            splash:go(splash.args.url) 
            splash:runjs('document.getElementsByClassName("choices")[1].getElementsByClassName("ui_checkbox item")[2].getElementsByTagName("input")[0].click();') 
            splash:wait(1) 
            return splash:html() 
        end
        """
        yield scrapy.Request(response.url, self.parse_solo_reviewers, meta={
            'splash': {
                'args': {'lua_source': script },
                'endpoint': 'execute',
            }
        })   

    def parse_business(self, response):
        script = """
        function main(splash)
            splash:go(splash.args.url) 
            splash:runjs('document.getElementsByClassName("choices")[1].getElementsByClassName("ui_checkbox item")[3].getElementsByTagName("input")[0].click();') 
            splash:wait(1) 
            return splash:html() 
        end
        """
        yield scrapy.Request(response.url, self.parse_business_reviewers, meta={
            'splash': {
                'args': {'lua_source': script },
                'endpoint': 'execute',
            }
        })  

    def parse_friends(self, response):
        script = """
        function main(splash)
            splash:go(splash.args.url) 
            splash:runjs('document.getElementsByClassName("choices")[1].getElementsByClassName("ui_checkbox item")[4].getElementsByTagName("input")[0].click();') 
            splash:wait(1) 
            return splash:html() 
        end
        """
        yield scrapy.Request(response.url, self.parse_friends_reviewers, meta={
            'splash': {
                'args': {'lua_source': script },
                'endpoint': 'execute',
            }
        })  

    
    def start_requests(self):
        url = 'https://www.tripadvisor.com.sg/Hotel_Review-g294265-d1086295-Reviews-Crowne_Plaza_Changi_Airport-Singapore.html'
        for x in range(5):   
            if x == 0:
                print("Start request 0")
                yield scrapy.Request(url=url, callback=self.parse_families)
            elif x == 1:
                print("Start request 1")
                yield scrapy.Request(url=url, callback=self.parse_couples)
            elif x == 2:
                print("Start request 2")
                yield scrapy.Request(url=url, callback=self.parse_solo)
            elif x == 3:
                print("Start request 3")
                yield scrapy.Request(url=url, callback=self.parse_business)
            elif x == 4:
                print("Start request 4")
                yield scrapy.Request(url=url, callback=self.parse_friends)
            else:
                print("Invalid")
                

         
    def parse_families_reviewers(self,response):
        print("Families")
        yield scrapy.Request(callback=self.start_requests)
        
    def parse_couples_reviewers(self,response):
        print("Couples")
        yield scrapy.Request(callback=self.start_requests)
        
    def parse_solo_reviewers(self,response):
        print("Solo")
        yield scrapy.Request(callback=self.start_requests)
        
    def parse_business_reviewers(self,response):
        print("Biz")
        yield scrapy.Request(callback=self.start_requests)

    def parse_friends_reviewers(self,response):
        print("Friends")
        yield scrapy.Request(callback=self.start_requests)