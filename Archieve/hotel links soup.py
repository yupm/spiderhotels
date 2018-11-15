import requests
import re
import time
import csv
from random import randint
from bs4 import BeautifulSoup as soup

Name=[]
Website=[]
Scores=[]
Pages=[]
    
link = "https://www.tripadvisor.com.sg/Hotels-g294265-Singapore-Hotels.html#BODYCON"
s = requests.Session()
page = s.get(link)
soup_page = soup(page.content, "html.parser")
container_0 = soup_page.findAll("div",{"class":"pageNumbers"})

total_pages = int(re.search(r'\d+|$',re.sub("(?s:.*)last', ", "",str(container_0)))[0])
reviews_per_page = len(soup_page.findAll("div",{"class":"listing_title"}))

for x in range(0,(total_pages-1)*reviews_per_page+1,reviews_per_page):

    if (x==0) :
        pass
    else :
        link = "https://www.tripadvisor.com.sg/Hotels-g294265-oa" +str(x)+ "-Singapore-Hotels.html#BODYCON"
        
    page = s.get(link)
    soup_page = soup(page.content, "html.parser")
    Pages.append(soup_page) 
    container_1 = soup_page.findAll("div",{"class":"listing_title"})
    
    for items in container_1:
        hlink = re.sub(r'.*href="', '', str(items))
        hlink = re.sub(r'" id=".*', '', str(hlink))
        Website.append ('https://www.tripadvisor.com.sg' + hlink)
        
        Hname = re.sub(r'.*target="_blank">', '', str(items))
        print(re.sub(r'</.*', '', str(Hname)))
        Name.append (re.sub(r'</.*', '', str(Hname)))
            
    print(x)


with open('Hotel_Links.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(Name, Website))
    f.close()
    
with open('Page_sources.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(zip(Pages))
    f.close()
    
