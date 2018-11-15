from bs4 import BeautifulSoup;
from appconst import HTMLTag, AppConfig as app_config
import re

def wp_parse_html(html_content):
    return BeautifulSoup(html_content, 'html.parser')


def wp_check_element_none(selected_elem):
    return selected_elem is None or len(selected_elem) == 0


def wp_select_css(html_parsed, css_selector, idx=0):
    elem_selected = html_parsed.select(css_selector)

    if wp_check_element_none(elem_selected):
        print('no elem selected ' + str(elem_selected))
        return "null"
    else:
        return elem_selected[idx]

def wp_select_css_attrval_from_html(html_parsed, css_selector, attr_key):
    elem_selected = html_parsed.select(css_selector)

    if wp_check_element_none(elem_selected):
        print('no elem selected ' + str(elem_selected))
        return "null"
    else:
        print('elem selected has attr val :' + elem_selected[0].attrs[attr_key])
        return str(elem_selected[0].attrs[attr_key])

def wp_select_css_text_from_html(html_parsed, css_selector):
    elem_selected = html_parsed.select(css_selector)

    if wp_check_element_none(elem_selected):
        print('no elem selected ' + str(elem_selected))
        return "null"
    else:
        #print('elem selected has text :' + elem_selected[0].getText())
        return str(elem_selected[0].getText())


def wp_select_css_is_element_present(html_parsed, css_selector):
    elem_selected = html_parsed.select(css_selector)

    if wp_check_element_none(elem_selected):
        print('no elem selected ' + str(elem_selected))
        return False
    else:
        print('elem selected has text :' + elem_selected[0].getText())
        return True