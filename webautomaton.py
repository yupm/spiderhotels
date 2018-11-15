from selenium import webdriver;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions;
from selenium.webdriver.common.by import By;
from selenium.common.exceptions import TimeoutException, NoSuchElementException;
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# path_to_extension = r'C:\Users\Decki\Desktop\aaa\3.2_1'

global chrome_options
chrome_options = Options()
chrome_options.add_argument('--headless')
# chrome_options.add_argument('load-extension=' + path_to_extension)

try:
    from urlparse import urljoin  # Python2
except ImportError:
    from urllib.parse import urljoin  # Python3


def joinURL(join1, join2):
    return urljoin(join1, join2)  # fix more than 2 arr


# todo: automate installation for chrome webdriver
global chromeDriver;


def wa_timeoutexception(e):
    TimeoutException(e)


def wa():
    global chromeDriver
    return chromeDriver


# todo: failed to get. check sel error for network e.g.
def wa_connect(url):
    global chromeDriver
    global chrome_options
    chromeDriver = webdriver.Chrome(chrome_options=chrome_options);
    chromeDriver.create_options()
    chromeDriver.set_window_size(1920, 1080);
    chromeDriver.get(url)


def wa_close():
    global chromeDriver
    chromeDriver.quit() #too many processes!!

def wa_click_by_css_with_offset(css_string, xoffset, yoffset):
    global chromeDriver
    ActionChains(chromeDriver).move_to_element_with_offset(chromeDriver.find_element_by_css_selector(css_string), xoffset, yoffset).click().perform()


def wa_get_html():
    global chromeDriver
    return chromeDriver.page_source


def wa_get_innerhtml_from_webelement(webelement):
    return webelement.get_attribute('innerHTML')


def wa_click_by_css(css_string):
    chromeDriver.find_element_by_css_selector(css_string).click()


def wa_click_by_css(css_string, idx=0):
    try:
        chromeDriver.find_elements_by_css_selector(css_string)[idx].click()
    except IndexError:
        print('not clicking. index err')


def wa_find_by_css(css_string):
    global chromeDriver
    return chromeDriver.find_element_by_css_selector(css_string)


def wa_wait_until_css_hastext(duration, css_string, text):
    global chromeDriver
    WebDriverWait(chromeDriver, duration).until(
        expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, css_string),
                                                          text))


def wa_wait_until_window_count(duration, window_count):
    global chromeDriver
    WebDriverWait(chromeDriver, duration).until(
        expected_conditions.number_of_windows_to_be(window_count))


def wa_wait_until_element_presence(duration, css_string):
    global chromeDriver
    WebDriverWait(chromeDriver, duration).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_string)))


def wa_wait_until_element_clickable(duration, css_string):
    global chromeDriver
    WebDriverWait(chromeDriver, duration).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, css_string)))
