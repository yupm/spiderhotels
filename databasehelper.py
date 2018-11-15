import csv;
from uuid import getnode as get_mac
from datetime import datetime
from pymongo import MongoClient

#default port for mongodb is 27017
client= MongoClient('', 27017)
db = client.ke5106_db
db.authenticate('', '')


#Collections
reviews = db.reviews
scraping_list = db.scraping_list
facility_score = db.facility_score
happy_checkin = db.happy_checkin
nearby = db.nearby
score_breakdown = db.score_breakdown
hotel_info = db.hotel_info
hotel_amenities = db.hotel_amenities

#Configuration
config = db.config
current_config_version = 0.1

#Exception handling
current_hotel_exception = ""
exception_retries = 0

#GETS THE COMPUTER'S MAC ADDRESS. THIS IS YOUR UNIQUE IDENTIFIER FOR THE MUTEX LOCK
mac_address = str(get_mac())
obfuscate_mac = str(int(mac_address[:7]) * (int(mac_address[8:]) + 1337))
cpu_id = obfuscate_mac

def gen_cpu_id():
    global cpu_id
    mac_address = str(get_mac())
    obfuscate_mac = str(int(mac_address[:7]) * (int(mac_address[8:]) + 1337))
    cpu_id = obfuscate_mac   
    print("My cpu id is: ", cpu_id)


def get_cpu_id():
    global cpu_id
    return cpu_id
    
#TO BE ONLY USED ONCE. DO NOT USE WITHOUT ASKING IN CHAT
'''
def initialize_scaper(): 
    print("Initializing")
    with open('Hotel_Links.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for i,row in enumerate(reader):
            if i > 0:
                hotel_name = row[0];
                website = {
                    'hotel_name': hotel_name,
                    'hotel_url': row[1],
                    'processed': False,
                    'proceed_page': 'init',
                    'processed_on': 'null',
                    'mutex' : 'null'      
                }                   
                scraping_pool.insert_one(website)
                print(hotel_name)
                print(row[1])
'''
#TO BE ONLY USED ONCE. DO NOT USE WITHOUT ASKING IN CHAT


def get_current_hotel_to_scrape():
    url = ''
    hid = ''
    name ='' 
    mtex_status = 'null'
    #First check db if there is a currently hotel that is locked by user
    mutex_hotel =  scraping_list.find_one({'mutex' : cpu_id})
    if mutex_hotel:
        print("Resuming")
        url = mutex_hotel['proceed_page']
        hid = mutex_hotel['_id']
        name =mutex_hotel['hotel_name'] 
        mtex_status = mutex_hotel['mutex'] 
    else:
        #if none, then get the list and find a hotel to scrape
        print("Get New")
        hotels = scraping_list.find()
        for hotel in hotels:
            if not hotel['processed'] and hotel['mutex'] == 'null':
                url = hotel['hotel_url']
                name = hotel['hotel_name']
                hid = hotel['_id']
                if hotel['proceed_page'] != 'init':
                    url = hotel['proceed_page']
                break
        if not hotels:
            print("ALL HOTELS HAVE BEEN SCRAPPED!")
    return url, hid, mtex_status, name

               
def lock_hotel_to_scrape(hotel_id):
    global cpu_id
    scraping_list.update_one({ '_id': hotel_id } , {'$set': { 'mutex' : cpu_id }})
    
def unlock_mutex(hotel_id):
    scraping_list.update_one({ '_id': hotel_id } , {'$set': { 'mutex' : 'null' }})

#checks that hotel is still lock on this comp id
def final_check_hotel_to_scrape(hotel_id):
    global cpu_id
    current_hotel = scraping_list.find_one({ '_id': hotel_id })
    if current_hotel['mutex'] == cpu_id:
        print("Currently holding mutex")
        return True
    else:
        print("Someone else is scaping, find another")
        return False     

#update that hotel is processed
def processed_hotel(hotel_id):
    scraping_list.update_one({ '_id': hotel_id } , 
                                 {
                                        '$set': { 
                                        'processed': True,
                                        'processed_on': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                        'mutex' : 'null'      
                                    } 
                                }
                            )

#update the current page being scrapped to resume                
def update_current_hotel_page(hotel_id, current_page_url):
    scraping_list.update_one({ '_id': hotel_id } , 
                                 {
                                        '$set': { 
                                        'proceed_page': current_page_url,
                                        'mutex' : cpu_id      
                                    } 
                                }
                            )
    
    
                
def save_ta_review_v2(output_row):
    hotel_name = output_row[0];
    hotel_locality = output_row[1];
    user_review_ta_id= output_row[2];
    is_owner_fav= output_row[3];
    is_via_mobile= output_row[4];
    user_name = output_row[5];
    user_locality= output_row[6];
    user_review_date= output_row[7];
    user_review_title= output_row[8];
    user_review_content= output_row[9];
    user_overall_rating= output_row[10];                    
    user_stayed_date= output_row[11];
    user_stayed_travel_type= output_row[12];
    if len(output_row) == 22:
        user_rating_5_given = output_row[13];
        user_rating_4_given= output_row[14];
        user_rating_3_given= output_row[15];
        user_rating_2_given= output_row[16];
        user_rating_1_given= output_row[17];                    
        user_stat_contribution= output_row[18];
        user_stat_visitedcity= output_row[19];
        user_stat_helpfulvotes= output_row[20];
        user_stat_photos = output_row[21];
    else:
        user_rating_5_given = "null";
        user_rating_4_given= "null";
        user_rating_3_given= "null";
        user_rating_2_given= "null";
        user_rating_1_given= "null";                    
        user_stat_contribution= "null";
        user_stat_visitedcity= "null";
        user_stat_helpfulvotes= "null";
        user_stat_photos = "null";
    
    review = {
        'ta_hotel_name' : hotel_name,
        'hotel_locality' : hotel_locality,
        'user_review_ta_id': user_review_ta_id,
        'is_owner_fav': is_owner_fav,
        'is_via_mobile': is_via_mobile,
        'user_name': user_name,
        'user_locality': user_locality,
        'user_review_date': user_review_date,
        'user_review_title': user_review_title,
        'user_review_content': user_review_content,
        'user_overall_rating': user_overall_rating,
        'user_stayed_date' : user_stayed_date,       
        'user_stayed_travel_type': user_stayed_travel_type,
        'user_rating_5_given': user_rating_5_given,
        'user_rating_4_given': user_rating_4_given,
        'user_rating_3_given': user_rating_3_given,
        'user_rating_2_given' : user_rating_2_given,
        'user_rating_1_given': user_rating_1_given,     
        'user_stat_contribution': user_stat_contribution,
        'user_stat_visitedcity': user_stat_visitedcity,
        'user_stat_helpfulvotes': user_stat_helpfulvotes,
        'user_stat_photos' : user_stat_photos  

        }      
    reviews.update_one({ 'user_review_ta_id': user_review_ta_id } , {'$set': review },upsert=True)
    print("Review saved: ", user_review_ta_id)

def save_ta_review(cur_review_id, 
                current_hotel_id, 
                is_curr_hotel_owner_fav_review,
                is_via_mobile,
                member_info_username,
                member_info_country,
                quote_title_url,
                review_content,
                review_rating,
                stayed_details_datestring,
                stayed_details_traveltype):
    review = {
        'review_id' : cur_review_id,
        'hotel_id': current_hotel_id,
        'is_curr_hotel_owner_fav_review': is_curr_hotel_owner_fav_review,
        'is_via_mobile': str(is_via_mobile),
        'member_info_username': member_info_username,
        'member_info_country': member_info_country,
        'quote_title_url': quote_title_url,
        'review_content': review_content,
        'review_rating': review_rating,
        'stayed_details_datestring': stayed_details_datestring,
        'stayed_details_traveltype' : stayed_details_traveltype      
        }      
    reviews.update_one({ 'review_id': cur_review_id } , {'$set': review },upsert=True)
    print("Review saved")



def insert_facility_score(hotel_id, 
                        facility1, 
                        facility2,
                        facility3,
                        facility4,
                        facility5):
    facility = {
        'hotel_id' : hotel_id,
        'facility1': facility1,
        'facility2': facility2,
        'facility3': facility3,
        'facility4': facility4,
        'facility5': facility5,
        }      
    facility_score.update_one({ 'hotel_id': hotel_id } , {'$set': facility },upsert=True)


def insert_happy_checkin(hotel_id, score):
    happy_score = {
        'hotel_id' : hotel_id,
        'happy_checkin': score
        }      
    happy_checkin.update_one({ 'hotel_id': hotel_id } , {'$set': happy_score },upsert=True)
    
    
def insert_nearby(hotel_id, poi, proximity):
    nearby_place = {
        'hotel_id' : hotel_id,
        'nearby_place': poi,
        'proximity': proximity
        }      
    nearby.update_one({ 'hotel_id': hotel_id,'nearby_place': poi } , {'$set': nearby_place },upsert=True)
 
def insert_hotel_info(hotel_id, key, value):
    hotel_info.update_one({ 'hotel_id': hotel_id } , {'$set': {key: value} },upsert=True)
    

def get_hotel_info_by_id(hotel_id): 
    hotel = hotel_info.find_one({'hotel_id' : hotel_id})
    return hotel

def get_hotel_info_by_postal(hotel_id): 
    hotel = hotel_info.find_one({'postalCode' : hotel_id})
    return hotel


def get_reviews():
    review_list = reviews.find()
    return review_list

def insert_review_value(review_id, key, value):
    hotel_info.update_one({ 'user_review_ta_id': review_id } , {'$set': {key: value} },upsert=True)


def insert_hotel_amenities(hotel_name, hotel_postal, amenity):
    hotel_amenities.update_one({ 'hotel_name': hotel_name, 'postalCode': hotel_postal } , {'$push': { 'amenities': amenity} },upsert=True)
    

def insert_score_breakdown(hotel_id, param1, param2, param3, param4, param5, overall, badge):
    hotel_score = {
        'hotel_id' : hotel_id,
        'param1': param1,
        'param2': param2,
        'param3': param3,
        'param4': param4,
        'param5': param5,
        'overall': overall,
        'badge': badge,
        }  
    score_breakdown.update_one({ 'hotel_id': hotel_id } , {'$set': hotel_score },upsert=True)

    
def set_review_scrape_limit(limit):
    config.update_one({ 'config_version': current_config_version } , {'$set': {'review_scrape_limit': 1000 } },upsert=True)
    
    
def get_review_scrape_limit():
    configuration = config.find_one({ 'config_version': current_config_version })
    return configuration['review_scrape_limit']

def get_review_max_retries():
    configuration = config.find_one({ 'config_version': current_config_version })
    return configuration['max_retries']


def notify_exception(hotel_id):
    global current_hotel_exception
    global exception_retries
    
    if hotel_id == current_hotel_exception:    
        exception_retries = exception_retries + 1
        print("Number of retries for hotel is : ", exception_retries)
    else:
        print("Initiate new hotel retry")
        exception_retries = 0
        current_hotel_exception = hotel_id
    
    max_retries = get_review_max_retries()
    if exception_retries > max_retries:
       print("Locking hotel")
       lock_hotel_for_error(hotel_id);
    
def lock_hotel_for_error(hotel_id):
    global cpu_id
    print("Locking down hotel id for troubleshooting: " , hotel_id)
    scraping_list.update_one({ '_id': hotel_id } , {'$set': { 'mutex' : "lock" }})
   