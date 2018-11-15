from appconst import HTMLTag, AppConfig as app_config
from csvwriter import cvw_init_with_header, cvw_write_row
from webautomaton import urljoin, wa_connect, wa_find_by_css, wa_click_by_css, wa_wait_until_css_hastext, \
    wa_get_html, TimeoutException, NoSuchElementException, wa_close, wa, wa_wait_until_window_count, \
    wa_wait_until_element_clickable
from webparser import wp_parse_html, wp_select_css_text_from_html,wp_select_css
from webautomatonhelper import wah_tripad_newsignupadcheck

# create csv
# taxishuttles-thailand-phuket.csv
# taxishuttles-thailand-kosamui.csv
# taxishuttles-indonesia-batam
cvw_init_with_header('taxishuttles-indonesia-bali.csv',
                     ['COMPANY_NAME',
                      'ADDRESS',
                      'RANK',
                      'TELEPHONE',
                      'WEBSITE',
                      'OVERALL_RATING',
                      'TOTAL_REVIEW_COUNT'
                      ])
# /Attractions-g297717-Activities-c59-t182-Batam_Riau_Archipelago_Riau_Islands_Province.html
# /Attractions-g293918-Activities-c59-t182-Ko_Samui_Surat_Thani_Province.html
# /Attractions-g293920-Activities-c59-oa00-t182-ca00-Phuket.html
# /Attractions-g294226-Activities-c59-t182-oa00-Bali.html
TAXI_SHUTTLE_URL = "/Attractions-g294226-Activities-c59-t182-oa00-Bali.html"
FQDN_TAXI_SHUTTLE_URL = urljoin(app_config.fqdn, TAXI_SHUTTLE_URL);

global hotel_reviews_listing_index
hotel_reviews_listing_index = 0

global taxi_shuttle_detailed_url_arr
taxi_shuttle_detailed_url_arr = []


def getTaxiShuttleMainInfo(url_path):
    wa_connect(url_path)

    # handle ads
    wah_tripad_newsignupadcheck()

    # parse html
    taxi_shuttle_main_html = wa_get_html()

    taxi_shuttle_main_parsed = wp_parse_html(taxi_shuttle_main_html)

    heading = wp_select_css_text_from_html(taxi_shuttle_main_parsed, '#HEADING')
    print('heading :' + heading)

    locality = wp_select_css_text_from_html(taxi_shuttle_main_parsed, '.locality')
    print('locality :' + locality)

    rank = wp_select_css_text_from_html(taxi_shuttle_main_parsed, '.header_popularity span')
    print('rank :' + rank)

    phone = wp_select_css_text_from_html(taxi_shuttle_main_parsed, '.phone')
    print('phone :' + phone)

    reviews_overall_rating = wp_select_css_text_from_html(taxi_shuttle_main_parsed, '.rating .overallRating')
    print('reviews_overall_rating :' + reviews_overall_rating)

    reviews_total_count = wp_select_css_text_from_html(taxi_shuttle_main_parsed, '.rating .seeAllReviews')
    print('reviews_total_count :' + reviews_total_count)

    website_url = "null"

    try:
        waa = wa();
        waa_before = waa.window_handles[0]
        print('waa_before ' + waa_before)

        wa_wait_until_element_clickable(10, '.website .taLnk')
        wa_click_by_css('.website .taLnk')

        wa_wait_until_window_count(30, 2)

        waa_after = waa.window_handles[1]
        print('waa_after ' + waa_after)

        waa.switch_to.window(waa_after)

        website_url = waa.current_url;
        print(website_url)

        waa.close()
        waa.switch_to.window(waa_before)
        waa.close()


    except TimeoutException:
        print('cant click on website link. moving on...')
        pass
    except NoSuchElementException:
        print('no website assigned so moving on...')
        pass

    cvw_write_row([
        heading,
        locality,
        rank,
        phone,
        website_url,
        reviews_overall_rating,
        reviews_total_count
    ])


def getAllTaxiAndShuttles(url_path):
    global hotel_reviews_listing_index
    global taxi_shuttle_detailed_url_arr
    taxi_shuttle_html = None

    wa_connect(url_path);

    # set the search to be only at the designated location in the event TA suggest geobroaden, if any
    try:
        wa_wait_until_element_clickable(5, '#geobroaden_opt_out #secondaryText')
        wa_click_by_css('#geobroaden_opt_out #secondaryText')

        wa_wait_until_css_hastext(10, '#geobroaden_opt_in #secondaryText', 'Expand your search')

    except TimeoutException:

        print("error: no geobroaden option clicakble. Moving on...");

    taxi_shuttle_html = wa_get_html()

    taxi_shuttle_parsed = wp_parse_html(taxi_shuttle_html);

    #FIXME:replace find_all
    taxi_shuttle_element = taxi_shuttle_parsed.find_all(HTMLTag.tag_div, {'class': 'attraction_element'});

    # print(curr_hotel_details_review_containers)

    for idx, curr_taxi_shuttle in enumerate(taxi_shuttle_element):
        print(str(idx) + '--------------')
        taxi_shuttle_link = curr_taxi_shuttle.select('.listing_info a')[0]['href']
        print(taxi_shuttle_link)
        taxi_shuttle_detailed_url_arr.append(taxi_shuttle_link)

    # check for next page
    try:
        wa_find_by_css('.nav.next.rndBtn.ui_button.primary.taLnk')
        print('still got more taxis and shuttles!')

        # move to next page
        taxi_shuttle_listing_page_no = taxi_shuttle_listing_page_no + 30

        # TODO: CLOSE WINDOW! capture the current one before moving on.

        getAllTaxiAndShuttles(
            urljoin(app_config.fqdn, TAXI_SHUTTLE_URL.replace('oa00', 'oa' + str(taxi_shuttle_listing_page_no))))


    except NoSuchElementException:
        print('no more taxi and shuttles! closing..')
        wa_close();
        print('printing detailed')

        for idx, curr_taxi_shuttle_detailed_url in enumerate(taxi_shuttle_detailed_url_arr):
            if idx >= 151:
                getTaxiShuttleMainInfo(urljoin(app_config.fqdn, curr_taxi_shuttle_detailed_url))

        # sys.exit(0);


getAllTaxiAndShuttles(FQDN_TAXI_SHUTTLE_URL)
