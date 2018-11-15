# windows lxml2 installation
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

from bs4 import BeautifulSoup
import re
import csv
import time
from selenium import webdriver

chromeDriver = webdriver.Chrome()
chromeDriver.set_window_size(1920, 1080)

global hotel_listing_index
hotel_listing_index = 0
Name=[]
Website=[]

def getHotelsFromUrl(urlPath):
    chromeDriver.get(urlPath)
    global hotel_listing_index
    
    try:
        curr_page_html = chromeDriver.page_source
        curr_page = BeautifulSoup(curr_page_html, 'html.parser')
        curr_hotel_containers = curr_page.find_all('div', {'class': 'listing_title'})
            
        for items in curr_hotel_containers:
            hlink = re.sub(r'.*href="', '', str(items))
            hlink = re.sub(r'" id=".*', '', str(hlink))
            Website.append ('https://www.tripadvisor.com.sg' + hlink)
                      
            Hname = re.sub(r'.*target="_blank">', '', str(items))
            Name.append (re.sub(r'</.*', '', str(Hname)))
                
    except :
        print("error: fail to load full content")
    
    hotel_listing_index = hotel_listing_index + 1
    last_page = int(re.search(r'\d+|$',re.sub("(?s:.*)last', ", "",str(curr_page.findAll("div",{"class":"pageNumbers"}))))[0])
    if last_page == 0:
        print('Completed! ' )
        print('Reached last page! closing..')
        chromeDriver.close()
        return
    else:
        time.sleep(3)
        print('Completed page '+ str(hotel_listing_index) + '/' + str(last_page) + ' of hotel listings... proceeding to next page...' )
        getHotelsFromUrl("https://www.tripadvisor.com.sg/Hotels-g294265-oa" +str(hotel_listing_index*30)+ "-Singapore-Hotels.html#BODYCON")

getHotelsFromUrl('https://www.tripadvisor.com.sg/Hotels-g294265-oa00-Singapore-Hotels.html')                          


headings = ['Name','Link']

with open("Hotel_Links.csv", "w", newline="", encoding="utf-8") as f: 
    writer = csv.writer(f)
    writer.writerow(headings)
    writer.writerows(zip(Name, Website))
    f.close()