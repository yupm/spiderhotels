import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get("https://sg.hotels.com/search.do?resolved-location=CITY%3A1655844%3AUNKNOWN%3AUNKNOWN&destination-id=1655844&q-destination=Singapore,%20Singapore&q-check-in=2019-06-01&q-check-out=2019-06-02&q-rooms=1&q-room-0-adults=2&q-room-0-children=0")
time.sleep(5)

elem = browser.find_element_by_tag_name("body")

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Pause to load page
    time.sleep(5)
    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

post_elems = browser.find_elements_by_class_name("p-name")

master_list=[]

for post in post_elems:
    curr_hotel = []
    hotel_id = post.find_element_by_xpath("a").get_attribute("href").split('/')[3]
    if hotel_id == 'travelads':
        continue
    hotel_name = post.text # Hotel name
    hotel_url = post.find_element_by_xpath("a").get_attribute("href").split('?')[0]
    curr_hotel.append(hotel_id)
    curr_hotel.append(hotel_name)
    curr_hotel.append(hotel_url)
    master_list.append(curr_hotel)
    
headings = ['hotel_id',
            'hotel_name',
            'hotel_url']

with open("hotel_com_output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headings)
    writer.writerows(master_list)
    
# 359 additional hotels are not available on your travel dates.
# JB and Batam hotels included.