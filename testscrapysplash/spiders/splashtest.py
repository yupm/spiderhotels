import scrapy
from scrapy_splash import SplashRequest
from scrapy.shell import inspect_response

#this function can toggle between the 5 choices, however note that it has be be hardcoded, e.g getElementsByClassName("ui_checkbox item")[2]

class SplashSpider(scrapy.Spider):
    name = "splashtest"

    start_urls = [
        'https://www.tripadvisor.com.sg/Hotel_Review-g294265-d1086295-Reviews-Crowne_Plaza_Changi_Airport-Singapore.html',
    ]
        

    def start_requests(self):
        script = """
        function main(splash)
            splash:go(splash.args.url) 
            splash:runjs('document.getElementsByClassName("choices")[1].getElementsByClassName("ui_checkbox item")[2].getElementsByTagName("input")[0].click();') 
            splash:wait(1) 
            return splash:html() 
        end
        """
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'args': {'lua_source': script},
                    'endpoint': 'execute',
                }
            })

    def parse(self, response):
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        # ...
         inspect_response(response, self)
         
        