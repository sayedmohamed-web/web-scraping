from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        # scroll odown to the bottom
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

        # wait the page to load
        time.sleep(scroll_pause_time)

        # get new scroll height and compare it to the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if last_height == new_height:
            # if heights are the same exit the function
            break
        last_height = new_height

driver = webdriver.Firefox()
driver.get('https://play.google.com/store/apps/details?id=com.adobe.reader&hl=en_US&gl=US&showAllReviews=true')
driver.implicitly_wait(5)
scroll(driver, 5)
more_btn = driver.find_element_by_link_text('Show More')