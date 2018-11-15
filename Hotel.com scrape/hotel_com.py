import requests
from requests.adapters import HTTPAdapter
import json
import csv
import time
from random import randint
from bs4 import BeautifulSoup as soup
import re
import sys
sys.path.append('..')

import databasehelper as db


s = requests.Session()
s.mount('https://', HTTPAdapter(max_retries=10))

master_list=[]



print("Time to get hotel info")    
# Read master_list
with open('hotels_com_output.csv', 'r') as f:
    reader = csv.reader(f)
    master_list = list(reader)
master_list = master_list[1:]

'''
happy_checkin = []
nearby = []
overall_score = []
facilities_score = []
'''
h=0
for hotel in master_list:
    print("Looping for num times: ", h)
    h = h + 1
    current_hotel = []
    hotel_id = hotel[0]
    hotel_postal = hotel[2]
    hotel_link = hotel[4]
    num_retries = 5
    
    # What's around
    for attempt_no in range(num_retries):
        try:
            r = requests.get(hotel_link)
            time.sleep(randint(1,2))
            content = soup(r.content, "lxml")
            nearby_places = content.find("div", {"id": "overview-section-6"}).find("ul").findAll("li")
            postalcode = content.find("span", {"class": "postal-code"}).find("span")
            hotel_postal = postalcode.text    
            
            amenities_type = content.findAll("div", {"class": "fact-sheet-table-cell"})
            for amenities_table in amenities_type:
                amenities = amenities_table.findAll("li")
                for amenity in amenities:
                    db.insert_amenities(amenity.text, hotel_id)

            db.insert_hotel_info(hotel_id, "postalCode", hotel_postal)          
            
            break
        except AttributeError as error:
            if attempt_no < (num_retries - 1):
                print("Error encountered. Hotel: " + hotel_id + " Attempt: " + str(attempt_no+1))
                time.sleep(10)
            else:
                break
    
    # % happy with check-in
    r = requests.get('https://sg.hotels.com/hotel/' + str(hotel_id) + '/check_in_rating.json')
    current_hotel.append(hotel_id)
    try:
        temp_val = json.loads(r.text)['happyCheckInPercentage']
        db.insert_hotel_info(hotel_id, "happyCheckInPercentage", json.loads(r.text)['happyCheckInPercentage'])
    except KeyError:
        current_hotel.append('')
        
    '''    
    db_nearby = []   
    for place in nearby_places:
        current_place = []
        name = place.get_text().split(" - ")[0]
        proximity = place.get_text().split(" - ")[-1]
        if proximity == name:
            proximity = ''
        ###!!!! to change to digits
        current_place.append(name)
        print(name)
        current_place.append(proximity)
        print(proximity)
        db_nearby.append(current_place)
        
    
    if db_nearby:    
        db.insert_hotel_info(hotel_id, "nearby_places", db_nearby)
        '''
               
    # review score by category
    current_score = [hotel_id]
    current_facility = [hotel_id]
    
    for attempt_no in range(num_retries):
        try:
            r = requests.get(hotel_link + '-tr')
            print("Current page is: ", hotel_link + '-tr')
            time.sleep(randint(1,2))
            content = soup(r.content, "lxml")
        except AttributeError as error:
            if attempt_no < (num_retries - 1):
                print("Error encountered. Hotel: " + hotel_id + " Attempt: " + str(attempt_no+1))
                time.sleep(5)
            else:
                break
            
    try:
        review = content.find("div", {"class": "overall has-tt-icon tt-all"})
        review_overall_badge = review.find("div", {"class": "overall-score"}).find("span", {"class": "badge"}).text
        review_overall_rating = review.find("div", {"class": "overall-score"}).find("span", {"class": "rating"}).text
        review_score = review.findAll("div",{"class": "count"})
        review_facilities1 = review.findAll("li", {"class":"trust-you-review "})
        if not review_facilities1:
                review_facilities1 = review.findAll("li", {"class":"rating"})
        review_facilities2 = review.findAll("li", {"class":"trust-you-review hide-on-xs"})
        
        i = 5;
        for breakdown in review_score:
            #data_score_key = breakdown.get('data-score-key')
            breakdown_score = re.findall(r'\d+', breakdown.text)
            score_str =  str(breakdown_score[0])
            db.insert_hotel_info(hotel_id,"Ratings(" +str(i) + ")", int(score_str))
            i = i - 1;

        db.insert_hotel_info(hotel_id, "review_overall_rating", float(review_overall_rating))
        db.insert_hotel_info(hotel_id, "review_overall_badge", review_overall_badge)

        #db.insert_score_breakdown(current_score[0], current_score[1],current_score[2],
        #                          current_score[3],current_score[4],current_score[5],review_overall_rating, review_overall_badge)
            
        for review_facilities in (review_facilities1,review_facilities2):
            for breakdown in review_facilities:
                try:
                    current_category= breakdown.find("div", {"class": "category"}).text
                    current_category_score = str(str(breakdown).split(":")[1]).split("%")[0]
                    current_facility.append(current_category + ":" + current_category_score)
                    db.insert_hotel_info(hotel_id, current_category, current_category_score)

                except AttributeError as error: 
                    current_category= breakdown.find("h5", {"class":"label"}).text
                    current_category_score = breakdown.find("span", {"class":"value"}).text
                    current_facility.append(current_category + ":" + current_category_score)
                    db.insert_hotel_info(hotel_id, current_category, current_category_score)


        
    except AttributeError as error: 
            print('No review for hotel id:' + hotel_id )

