from webautomaton import wa_click_by_css, wa_wait_until_element_clickable, TimeoutException
import time

# Selenium + TripAdvisor Helper
def wah_tripad_newsignupadcheck():
    try:
        wa_wait_until_element_clickable(15, '.slide_up_messaging_container .close')

        # note: click x
        wa_click_by_css('.slide_up_messaging_container .close')

        # wait for the animation to close..
        time.sleep(10)

    except TimeoutException:
        print('cant find ad. moving on...')
        pass
