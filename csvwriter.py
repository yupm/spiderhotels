import csv;
import unicodedata;
from unidecode import unidecode;

global csv_writer
global csv_appender

# reference code.
def sanitize_deemojify(inputstr):
    returnstr = ""

    for character in inputstr:
        try:
            character.encode("ascii")
            returnstr += character
        except UnicodeEncodeError:
            replaced = unidecode(str(character))
            if replaced != '':
                returnstr += replaced
            else:
                try:
                    returnstr += "[" + unicodedata.name(character) + "]"
                except ValueError:
                    returnstr += "[x]"

    return returnstr


# fixme: pass in encoding
def cvw_init_with_header(filename, header_arr):
    global csv_writer

    csv_file = open(filename, 'w',  encoding='utf8')
    csv_writer = csv.writer(csv_file)

    if header_arr is not None:
        csv_writer.writerow(header_arr)


def cvw_write_row(write_arr):
    global csv_writer

    # fixme: try catch csv writer whether inited
    csv_writer.writerow(write_arr);

def csv_init_with_header(filename, header_arr):
    with open(filename, "a", newline="", encoding=" utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header_arr)
        f.close()


def csv_append_row(filename, write_arr):
    with open(filename, "a", newline="", encoding=" utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(write_arr)
        f.close()

#
#
# FULL_QUALIFIED_DOMAIN_NAME = 'https://www.tripadvisor.com.sg';
# global current_get_hotel_reviews_itemidx;
# global current_hotel_name;
# global output;
# output = [];
#
# with open('Hotel_Links.csv') as f:
#     reader = csv.reader(f, delimiter=',')
#     for i, row in enumerate(reader):
#         if not (row):
#             continue
#         if i > 10:
#             break
#         hotel_review_url = row[2].replace(FULL_QUALIFIED_DOMAIN_NAME, '');
#         fqdn_hotel_current_url = urljoin(FULL_QUALIFIED_DOMAIN_NAME, hotel_review_url);
#         current_get_hotel_reviews_itemidx = -1;
#         current_hotel_name = row[0];
#         getReviewsFromHotelUrl(fqdn_hotel_current_url);
#
# headings = ['hotel_name',
#             'is_curr_hotel_owner_fav_review',
#             'is_via_mobile',
#             'member_info_username',
#             'member_info_country',
#             'quote_title_url',
#             'review_content',
#             'review_rating',
#             'stayed_details_datestring',
#             'stayed_details_traveltype']
#
# with open("output.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(headings)
#     writer.writerows(output)
