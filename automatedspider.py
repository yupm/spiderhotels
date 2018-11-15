from scrapetahotel import get_hotel_details_from_url_db, scrapeTaHotelException
import databasehelper as db

db.gen_cpu_id();
hotels_exists = True

while hotels_exists:
    try:
        hotel_info = db.get_current_hotel_to_scrape()       
        if hotel_info[0] != '':
            get_hotel_details_from_url_db(hotel_info[0], hotel_info[1],  hotel_info[2], hotel_info[3])
            db.processed_hotel(hotel_info[1])
        else:
            hotels_exists = False
    except scrapeTaHotelException as e:  # Exception list
        print('Getting into exception scrapetahotel')
        db.notify_exception(hotel_info[1])
       
