from appconst import HTMLTag, AppConfig as app_config
from csvwriter import cvw_init_with_header, cvw_write_row, csv_init_with_header, csv_append_row
from webautomaton import urljoin, wa_connect, wa_find_by_css, wa_click_by_css, wa_wait_until_css_hastext, \
    wa_get_html, wa_wait_until_element_presence, TimeoutException, NoSuchElementException, wa_close, \
    wa_wait_until_element_clickable, wa_get_innerhtml_from_webelement,  wa_click_by_css_with_offset
from webparser import wp_parse_html, wp_select_css_text_from_html, wp_select_css_is_element_present, \
    wp_check_element_none, wp_select_css_attrval_from_html

import re
import time

import databasehelper as db
csv_filename = ''

class scrapeTaHotelException(Exception):
    def __init__(self, last_idx_except):
        self.last_idx_except = last_idx_except

# create csv
def create_hotel_details_csv(hotel_name):
    cvw_init_with_header('./output/scrap-ta-hotel-' + hotel_name + '.csv',
                         ['HOTEL_LOCALITY',
                          'USER_REVIEW_TA_ID',
                          'IS_OWNER_FAV',
                          'IS_VIA_MOBILE',
                          'USER_NAME',
                          'USER_LOCALITY',
                          'USER_REVIEW_DATE',
                          'USER_REVIEW_TITLE',
                          'USER_REVIEW_CONTENT',
                          'USER_OVERALL_RATING',
                          'USER_STAYED_DATE',
                          'USER_STAYED_TRAVEL_TYPE',
                          'USER_RATING_5_GIVEN',
                          'USER_RATING_4_GIVEN',
                          'USER_RATING_3_GIVEN',
                          'USER_RATING_2_GIVEN',
                          'USER_RATING_1_GIVEN',
                          'USER_STAT_CONTRIBUTION',
                          'USER_STAT_VISITEDCITY',
                          'USER_STAT_HELPFULVOTES',
                          'USER_STAT_PHOTOS'
                          ])

def create_hotel_details_csv_single_line(hotel_name):
    global csv_filename
    csv_filename = './output/scrap-ta-hotel-' + hotel_name + '.csv'
    csv_init_with_header(csv_filename,
                         ['HOTEL_LOCALITY',
                          'USER_REVIEW_TA_ID',
                          'IS_OWNER_FAV',
                          'IS_VIA_MOBILE',
                          'USER_NAME',
                          'USER_LOCALITY',
                          'USER_REVIEW_DATE',
                          'USER_REVIEW_TITLE',
                          'USER_REVIEW_CONTENT',
                          'USER_OVERALL_RATING',
                          'USER_STAYED_DATE',
                          'USER_STAYED_TRAVEL_TYPE',
                          'USER_RATING_5_GIVEN',
                          'USER_RATING_4_GIVEN',
                          'USER_RATING_3_GIVEN',
                          'USER_RATING_2_GIVEN',
                          'USER_RATING_1_GIVEN',
                          'USER_STAT_CONTRIBUTION',
                          'USER_STAT_VISITEDCITY',
                          'USER_STAT_HELPFULVOTES',
                          'USER_STAT_PHOTOS'
                          ])

    
# scrapeurl = '/Hotel_Review-g294265-d5513299-Reviews-or00-Punggol_Ranch_Resort-Singapore.html'
global hotel_reviews_listing_index
hotel_reviews_listing_index = 0

global user_rating_breakdown_levels
user_rating_breakdown_levels = 5

# contribution, city visited, helpful vote, photos. NOTE: not in order.
global user_contribution_breakdown_levels
user_contribution_breakdown_levels = 4

global hotel_base_url
hotel_base_url = ''

global idx_to_retry
idx_to_retry = 0

def get_array_of_user_contrib(user_contrib_breakdown_selected):
    user_contribution_arr = ["null"] * user_contribution_breakdown_levels
    for idxx, contrib_score in enumerate(user_contrib_breakdown_selected):
        contrib_score_text = (str(contrib_score.getText()).strip())
        user_contrib_score_text_spittedarr = contrib_score_text.split(" ", 1)
        user_contrib_score_value = user_contrib_score_text_spittedarr[0]
        user_contrib_score_label = user_contrib_score_text_spittedarr[1]

        if user_contrib_score_label == 'Contribution' or user_contrib_score_label == 'Contributions':
            user_contribution_arr[0] = user_contrib_score_value
        elif user_contrib_score_label == 'City visited' or user_contrib_score_label == 'Cities visited':
            user_contribution_arr[1] = user_contrib_score_value
        elif user_contrib_score_label == 'Helpful vote' or user_contrib_score_label == 'Helpful votes':
            user_contribution_arr[2] = user_contrib_score_value
        elif user_contrib_score_label == 'Photo' or user_contrib_score_label == 'Photos':
            user_contribution_arr[3] = user_contrib_score_value

    print('user_contribution_arr :' + str(user_contribution_arr))
    return user_contribution_arr


def getReviews():
    return


def scrapeReview():
    return


def scrapeReviewUserOverlay():
    return


def get_hotel_details_from_url(hotel_details_url_path, hotel_details_name='', hotel_review_idx=0):
    try:
        global hotel_reviews_listing_index
        global user_rating_breakdown_levels
        global user_contribution_breakdown_levels
        global hotel_base_url
        global idx_to_retry

        # setting up for the first time the hotel is called.
        if hotel_details_name != '':
            hotel_reviews_listing_index = 0
            hotel_base_url = hotel_details_url_path
            create_hotel_details_csv(hotel_details_name)

        # if hotel review is > 0 , set listing index to the new review start idx and also update the hotel details url path
        if hotel_review_idx > 0:
            hotel_reviews_listing_index = hotel_review_idx
            hotel_details_url_path = hotel_details_url_path.replace('or00', 'or' + str(hotel_reviews_listing_index))
    
        # construct full hotel url path. assumes relative path scraped
        fqdn_hotel_details_url_path = urljoin(app_config.fqdn, hotel_details_url_path)
    
        # connect to url
        wa_connect(fqdn_hotel_details_url_path);
    
        try:
            # fixme: wait?
            wa_find_by_css('.review-container');
            print('still got reviews!')
        except NoSuchElementException:
            print('no more reviews!')
            pass
            # can add function call to run upon reaching the page where there is no more reviews
    
        # tap on more btn... to trigger all hidden content to show
        try:
    
            wa_wait_until_element_presence(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks')
            wa_wait_until_css_hastext(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks', 'More')
            wa_wait_until_element_clickable(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks')
            time.sleep(5)
            wa_click_by_css('.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks')
            # wa_wait_until_element_clickable(20, '.review-container .entry .partial_entry .taLnk.ulBlueLinks')
            # wa_click_by_css('.review-container .entry .partial_entry .taLnk.ulBlueLinks')
    
            wa_wait_until_css_hastext(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks', 'Show less')
    
            curr_hotel_details_html = wa_get_html()
    
            curr_hotel_details_parsed = wp_parse_html(curr_hotel_details_html);
    
            print("success: full content no ajax is ready");
    
            # todo: if 200
            # FIXME: ?get total reviews and see the number of pages needed
    
            # Get all the reviews div
            curr_hotel_details_locality = wp_select_css_text_from_html(curr_hotel_details_parsed,
                                                                       '.locality')
            print('is_curr_hotel_owner_fav_review is ' + str(curr_hotel_details_locality))
    
            curr_hotel_details_review_containers = curr_hotel_details_parsed.find_all(HTMLTag.tag_div,
                                                                                      {'class': 'review-container'});
            # print(curr_hotel_details_review_containers)
    
            for idx, curr_hotel_review_parsed in enumerate(curr_hotel_details_review_containers):
                output_row = []
                postalCode = re.findall(r'\d+', str(curr_hotel_details_locality))
                if postalCode:
                    output_row.append(postalCode[0])
                else:
                     #got geyland hotel no postal code.
                    #e.g. https://www.tripadvisor.com.sg/Hotel_Review-g294265-d3316258-Reviews-Darlene_Hotel-Singapore.html
                    output_row.append(curr_hotel_details_locality)
    
                # is hotel owner's fav review
                print('review # ' + str(idx) + '---------------------------------------')
    
                review_ta_id = wp_select_css_attrval_from_html(curr_hotel_review_parsed, '.reviewSelector', 'data-reviewid')
                print('review_ta_id is ' + review_ta_id)
                output_row.append(review_ta_id)
    
                is_curr_hotel_owner_fav_review = wp_select_css_is_element_present(curr_hotel_review_parsed,
                                                                                  '.ownerFavHeader')
                print('is_curr_hotel_owner_fav_review is ' + str(is_curr_hotel_owner_fav_review))
                output_row.append(str(is_curr_hotel_owner_fav_review));
    
                is_via_mobile = wp_select_css_is_element_present(curr_hotel_review_parsed,
                                                                 '.viaMobile')
                print('is_via_mobile is ' + str(is_via_mobile))
                output_row.append(str(is_via_mobile))
    
                member_info_username = wp_select_css_text_from_html(curr_hotel_review_parsed, '.member_info .info_text div')
                print('member_info_username is' + member_info_username)
                output_row.append(member_info_username)
    
                member_info_country = wp_select_css_text_from_html(curr_hotel_review_parsed,
                                                                   '.member_info .info_text .userLoc strong')
                print('member_info_country is ' + member_info_country)
                output_row.append(member_info_country)
    
                review_date = wp_select_css_attrval_from_html(curr_hotel_review_parsed, '.ratingDate', 'title')
                print('review_date is ' + review_date)
                output_row.append(review_date)
    
                review_title = wp_select_css_text_from_html(curr_hotel_review_parsed, '.noQuotes')
                print('review_title is ' + review_title)
                output_row.append(review_title)
    
                review_content = wp_select_css_text_from_html(curr_hotel_review_parsed, '.partial_entry')
                print('review_content is ' + review_content)
                output_row.append(review_content)
    
                # FIXME: add to Webparser module. also to consider multiple returns.
                review_rating_tag = curr_hotel_review_parsed.find(HTMLTag.tag_span,
                                                                  {HTMLTag.attr_class: re.compile('bubble_*')});
                # print(review_rating_tag);
                review_rating_tag_classes = dict(review_rating_tag.attrs)['class']
                # print(review_rating_tag_classes)
                # print(review_rating_tag_classes[-1])
                review_rating_tag_bubbleratingclass = review_rating_tag_classes[-1]
                review_rating_tag_bubbleratingvalue = review_rating_tag_bubbleratingclass.split('_')[-1]
                review_rating = review_rating_tag_bubbleratingvalue
                print('review rating is: ' + str(review_rating) + ' out of 50');
                output_row.append(str(review_rating));
    
                stayed_details = wp_select_css_text_from_html(curr_hotel_review_parsed, '.recommend-titleInline')
                stayed_details_datestring = 'null';
                stayed_details_traveltype = 'null';
    
                stayed_details_arr = stayed_details.split(',')
    
                # note: assume stayed date is minimum. bonus is the classification of traveller type.
                stayed_details_datestring = stayed_details_arr[0];
                if len(stayed_details_arr) > 1:
                    stayed_details_traveltype = stayed_details_arr[1];
    
                print('stayed_details_datestring is: ' + stayed_details_datestring);
                output_row.append(str(stayed_details_datestring))
                print('stayed_details_traveltype is: ' + stayed_details_traveltype);
                output_row.append(str(stayed_details_traveltype))
    
                # grab member
                try:
                    #todo: check ui_backdrop....
                    wa_wait_until_element_clickable(15, '.prw_rup.prw_reviews_member_info_resp .clickable')
                    wa_click_by_css_with_offset('.prw_rup.prw_reviews_member_info_resp .clickable', -50, -50)
                    time.sleep(2)
                    wa_click_by_css('.prw_rup.prw_reviews_member_info_resp .clickable',
                                    idx * 2)  # todo: cuz got 2 clickables per card
                    print('whats idx to clock : ' + str(idx))
    
                    wa_wait_until_element_presence(15, '.memberOverlay.simple.moRedesign')
                    member_overlay_selected = wa_find_by_css('.memberOverlay.simple.moRedesign')
                    member_overlay_parsed = wp_parse_html(wa_get_innerhtml_from_webelement(member_overlay_selected))
    
                    # user review ratings 0-5 breakdown
                    user_review_breakdown_selected = member_overlay_parsed.select('.rowCountReviewEnhancements')
    
                    if wp_check_element_none(user_review_breakdown_selected):
                        for i in range(user_rating_breakdown_levels):
                            output_row.append("null")
                    else:
                        for idxx, review_score in enumerate(user_review_breakdown_selected):
                            output_row.append(str(review_score.getText()))
                            print(str(review_score.getText()))
                        if len(user_review_breakdown_selected) < user_rating_breakdown_levels:
                            null_to_append_times = user_rating_breakdown_levels - len(user_review_breakdown_selected)
                            for i in range(null_to_append_times):
                                output_row.append("null")
    
                    # user review contributions breakdown
                    user_contribution_breakdown_selected = member_overlay_parsed.select('.badgeTextReviewEnhancements')
                    if wp_check_element_none(user_contribution_breakdown_selected):
                        for i in range(user_contribution_breakdown_levels):
                            output_row.append("null")
                    else:
                        for idxxx, user_contrib_score in enumerate(
                                get_array_of_user_contrib(user_contribution_breakdown_selected)):
                            output_row.append(user_contrib_score)

    
                    # kill off offending overlay. apparently no need to check for presence
                    wa_wait_until_element_clickable(15, '.ui_backdrop')
                    wa_click_by_css_with_offset('.ui_overlay.ui_popover.arrow_left', -50,-50)
                    #wa_click_by_css('.ui_backdrop')
                    time.sleep(3)
    
                except TimeoutException:
                    print('timed out click on member overlay. should THROW ERR...')
                    pass
                except NoSuchElementException:
                    print('No such element to click for member overlay. should THROW ERR too')
                    pass
    
                print('output row')
                print(output_row)
                cvw_write_row(output_row)
    
        except TimeoutException:
            print("error: fail to load full content");
    
        # check for next page
        try:
            wa_wait_until_element_presence(10, '#REVIEWS .nav.next.taLnk.ui_button.primary')
            print('still got more reviews!')
    
            # move to next page
            hotel_reviews_listing_index = hotel_reviews_listing_index + 5
    
            print('moving to the next listing index starting with:')
            print(hotel_reviews_listing_index)
    
            print('closing win and loading new')
            wa_close()
    
            idx_to_retry = hotel_reviews_listing_index

            # FOR TESTING: raise scrapeTaHotelException(idx_to_retry)
            get_hotel_details_from_url(
                urljoin(app_config.fqdn, hotel_base_url.replace('or00', 'or' + str(hotel_reviews_listing_index))))
    
        except TimeoutException:
            print('no more reviews! closing..')
            wa_close();
            print('printing detailed')
    
            # sys.exit(0);
    except:
        # all other errors
        raise scrapeTaHotelException(idx_to_retry)

def get_hotel_details_from_url_db(hotel_details_url_path, hotel_id, mtex_status, hotel_details_name=''):
    try:
        global hotel_reviews_listing_index
        global user_rating_breakdown_levels
        global user_contribution_breakdown_levels
        global hotel_base_url
        global csv_filename
        global idx_to_retry
        
        output_row = []
        print(" THE HOTEL PATH IS : ", hotel_details_url_path)
        # setting up for the first time the hotel is called. 
        csv_filename = './output/scrap-ta-hotel-' + hotel_details_name + '.csv'
        db.gen_cpu_id()
        cpu_id = db.get_cpu_id()
        print("My mutex status is : ", mtex_status, " and my cpu id is, ", cpu_id)
        if mtex_status != cpu_id:
            print("New instance, create csv header")
            create_hotel_details_csv_single_line(hotel_details_name)
            db.lock_hotel_to_scrape(hotel_id)
    
        print("Entry url", hotel_details_url_path)
        
        next_page = 0

        get_page_number = re.findall(r"(?<=-or)(.\d+)(?=\-)", hotel_details_url_path)
        if not get_page_number:
            hotel_details_url_path = re.sub(r"(?<=Reviews)(.)", "-or05-", hotel_details_url_path)
            idx_to_retry = 0
        else:          
            idx_to_retry = get_page_number[0]
            next_page = int(get_page_number[0]) + 5
            hotel_details_url_path = re.sub(r"(?<=-or)(.\d+)(?=\-)", str(next_page), hotel_details_url_path)
            
        # connect to url
        wa_connect(hotel_details_url_path);   
    
        try:
            # fixme: wait?
            wa_find_by_css('.review-container');
            print('still got reviews!')
        except NoSuchElementException:
            print('no more reviews!')
            pass
            # can add function call to run upon reaching the page where there is no more reviews

        # tap on more btn... to trigger all hidden content to show
        try:
            db.update_current_hotel_page(hotel_id, hotel_details_url_path)
            wa_wait_until_element_presence(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks')
            wa_wait_until_css_hastext(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks', 'More')
            wa_wait_until_element_clickable(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks')
            time.sleep(5)
            wa_click_by_css('.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks')
            # wa_wait_until_element_clickable(20, '.review-container .entry .partial_entry .taLnk.ulBlueLinks')
            # wa_click_by_css('.review-container .entry .partial_entry .taLnk.ulBlueLinks')
    
            wa_wait_until_css_hastext(20, '.prw_rup.prw_reviews_review_resp .taLnk.ulBlueLinks', 'Show less')
    
            curr_hotel_details_html = wa_get_html()
    
            curr_hotel_details_parsed = wp_parse_html(curr_hotel_details_html);
    
            print("success: full content no ajax is ready");
    
            # todo: if 200
            # FIXME: ?get total reviews and see the number of pages needed
    
            # Get all the reviews div
            curr_hotel_details_locality = wp_select_css_text_from_html(curr_hotel_details_parsed,
                                                                       '.locality')
            print('is_curr_hotel_owner_fav_review is ' + str(curr_hotel_details_locality))
    
            curr_hotel_details_review_containers = curr_hotel_details_parsed.find_all(HTMLTag.tag_div,
                                                                                      {'class': 'review-container'});
            # print(curr_hotel_details_review_containers)
    
            for idx, curr_hotel_review_parsed in enumerate(curr_hotel_details_review_containers):
                output_row = []
                output_row.append(hotel_details_name)
                postalCode = re.findall(r'\d+', str(curr_hotel_details_locality))
                if postalCode:
                    print(postalCode[0])
                    output_row.append(postalCode[0])
                else:
                    print(curr_hotel_details_locality)
                     #got geyland hotel no postal code.
                    #e.g. https://www.tripadvisor.com.sg/Hotel_Review-g294265-d3316258-Reviews-Darlene_Hotel-Singapore.html
                    output_row.append(curr_hotel_details_locality + hotel_details_name)
    
    
                # is hotel owner's fav review
                print('review # ' + str(idx) + '---------------------------------------')
    
                review_ta_id = wp_select_css_attrval_from_html(curr_hotel_review_parsed, '.reviewSelector', 'data-reviewid')
                print('review_ta_id is ' + review_ta_id)
                output_row.append(review_ta_id)
    
                is_curr_hotel_owner_fav_review = wp_select_css_is_element_present(curr_hotel_review_parsed,
                                                                                  '.ownerFavHeader')
               # print('is_curr_hotel_owner_fav_review is ' + str(is_curr_hotel_owner_fav_review))
                output_row.append(str(is_curr_hotel_owner_fav_review));
    
                is_via_mobile = wp_select_css_is_element_present(curr_hotel_review_parsed,
                                                                 '.viaMobile')
                #print('is_via_mobile is ' + str(is_via_mobile))
                output_row.append(str(is_via_mobile))
    
                member_info_username = wp_select_css_text_from_html(curr_hotel_review_parsed, '.member_info .info_text div')
                #print('member_info_username is' + member_info_username)
                output_row.append(member_info_username)
    
                member_info_country = wp_select_css_text_from_html(curr_hotel_review_parsed,
                                                                   '.member_info .info_text .userLoc strong')
                #print('member_info_country is ' + member_info_country)
                output_row.append(member_info_country)
    
                review_date = wp_select_css_attrval_from_html(curr_hotel_review_parsed, '.ratingDate', 'title')
                #print('review_date is ' + review_date)
                output_row.append(review_date)
    
                review_title = wp_select_css_text_from_html(curr_hotel_review_parsed, '.noQuotes')
                #print('review_title is ' + review_title)
                output_row.append(review_title)
    
                review_content = wp_select_css_text_from_html(curr_hotel_review_parsed, '.partial_entry')
                #print('review_content is ' + review_content)
                output_row.append(review_content)
    
                # FIXME: add to Webparser module. also to consider multiple returns.
                review_rating_tag = curr_hotel_review_parsed.find(HTMLTag.tag_span,
                                                                  {HTMLTag.attr_class: re.compile('bubble_*')});
                # print(review_rating_tag);
                review_rating_tag_classes = dict(review_rating_tag.attrs)['class']
                # print(review_rating_tag_classes)
                # print(review_rating_tag_classes[-1])
                review_rating_tag_bubbleratingclass = review_rating_tag_classes[-1]
                review_rating_tag_bubbleratingvalue = review_rating_tag_bubbleratingclass.split('_')[-1]
                review_rating = review_rating_tag_bubbleratingvalue
                #print('review rating is: ' + str(review_rating) + ' out of 50');
                output_row.append(str(review_rating));
    
                stayed_details = wp_select_css_text_from_html(curr_hotel_review_parsed, '.recommend-titleInline')
                stayed_details_datestring = 'null';
                stayed_details_traveltype = 'null';
    
                stayed_details_arr = stayed_details.split(',')
    
                # note: assume stayed date is minimum. bonus is the classification of traveller type.
                stayed_details_datestring = stayed_details_arr[0];
                if len(stayed_details_arr) > 1:
                    stayed_details_traveltype = stayed_details_arr[1];
    
                #print('stayed_details_datestring is: ' + stayed_details_datestring);
                output_row.append(str(stayed_details_datestring))
                #print('stayed_details_traveltype is: ' + stayed_details_traveltype);
                output_row.append(str(stayed_details_traveltype))
    
                # grab member
                try:
                    #todo: check ui_backdrop....
                    wa_wait_until_element_clickable(15, '.prw_rup.prw_reviews_member_info_resp .clickable')
                    wa_click_by_css_with_offset('.prw_rup.prw_reviews_member_info_resp .clickable', -50, -50)
                    time.sleep(2)
                    wa_click_by_css('.prw_rup.prw_reviews_member_info_resp .clickable',
                                    idx * 2)  # todo: cuz got 2 clickables per card
                    print('whats idx to clock : ' + str(idx))
    
                    wa_wait_until_element_presence(15, '.memberOverlay.simple.moRedesign')
                    member_overlay_selected = wa_find_by_css('.memberOverlay.simple.moRedesign')
                    member_overlay_parsed = wp_parse_html(wa_get_innerhtml_from_webelement(member_overlay_selected))
    
                    # user review ratings 0-5 breakdown
                    user_review_breakdown_selected = member_overlay_parsed.select('.rowCountReviewEnhancements')
    
                    if wp_check_element_none(user_review_breakdown_selected):
                        for i in range(user_rating_breakdown_levels):
                            output_row.append("null")
                    else:
                        for idxx, review_score in enumerate(user_review_breakdown_selected):
                            output_row.append(str(review_score.getText()))
                            print(str(review_score.getText()))
                        if len(user_review_breakdown_selected) < user_rating_breakdown_levels:
                            null_to_append_times = user_rating_breakdown_levels - len(user_review_breakdown_selected)
                            for i in range(null_to_append_times):
                                output_row.append("null")
    
                    # user review contributions breakdown
                    user_contribution_breakdown_selected = member_overlay_parsed.select('.badgeTextReviewEnhancements')
                    if wp_check_element_none(user_contribution_breakdown_selected):
                        for i in range(user_contribution_breakdown_levels):
                            output_row.append("null")
                    else:
                        for idxxx, user_contrib_score in enumerate(
                                get_array_of_user_contrib(user_contribution_breakdown_selected)):
                            output_row.append(user_contrib_score)
    
                    # kill off offending overlay. apparently no need to check for presence
                    wa_wait_until_element_clickable(15, '.ui_backdrop')
                    wa_click_by_css_with_offset('.ui_overlay.ui_popover.arrow_left', -50,-50)
                    #wa_click_by_css('.ui_backdrop')
                    time.sleep(3)
    
                except TimeoutException:
                    print('timed out click on member overlay. should THROW ERR...')
                    pass
                except NoSuchElementException:
                    print('No such element to click for member overlay. should THROW ERR too')
                    pass
    
                print('output row')
                print(output_row)
                csv_append_row(csv_filename, output_row)       
                try:                   
                    db.save_ta_review_v2(output_row)
                except:
                    print("FAILED")
    
        except TimeoutException:
            print("error: fail to load full content");
    
    
        # check for next page
        try:
            wa_wait_until_element_presence(10, '#REVIEWS .nav.next.taLnk.ui_button.primary')
            print('still got more reviews!')
    
    
            print('closing win and loading new')
            wa_close()
            
            max_scrape = db.get_review_scrape_limit()
            if next_page < max_scrape:
                print(max_scrape)
                if db.final_check_hotel_to_scrape(hotel_id):       
                    print("Exit url ", hotel_details_url_path)
                    get_hotel_details_from_url_db(hotel_details_url_path, hotel_id, mtex_status, hotel_details_name)
    
        except TimeoutException:
            print('no more reviews! closing..')
            wa_close();
            print('printing detailed')
    except:
        # all other errors
        raise scrapeTaHotelException(idx_to_retry)            