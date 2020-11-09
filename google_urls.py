from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import csv
import time


def all_links(url):
    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(
        'https://cloud.withgoogle.com/partners/?regions=EMEA_REGION&products=GOOGLE_WORKSPACE_PRODUCT&sort-type=RELEVANCE')
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'hats-close'))
        )
    finally:
        element.click()
        print('it all ok')
        driver.quit()


urls = all_links(
    'https://cloud.withgoogle.com/partners/?regions=EMEA_REGION&products=GOOGLE_WORKSPACE_PRODUCT&sort-type=RELEVANCE')

if urls:
    fields_name = urls[0].keys()
    with open('google_urls.csv', 'w', newline='') as outfile:
        dictwriter = csv.DictWriter(outfile, fields_name)
        dictwriter.writeheader()
        dictwriter.writerows(urls)
