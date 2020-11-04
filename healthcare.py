from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

url = 'https://experience.arcgis.com/experience/79cb51d21ecb4f58b3760192eace5428'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(10)

wait = WebDriverWait(driver, 30)
wait.until(EC.frame_to_be_available_and_switch_to_it(
    driver.find_element_by_class_name('iframe-widget_2')))
time.sleep(10)
driver.find_element_by_id('ember109').click()
time.sleep(10)

soup = BeautifulSoup(driver.page_source, 'html.parser')
if soup:
    nav = soup.find('nav', {'class', 'feature-list'})
else:
    print('error while parsing to soup object')

data = []
if nav:
    for span in nav.find_all(class_='flex-horizontal feature-list-item ember-view'):
        span_data = {}
        all_p = span.find_all('p')
        span_data['city'] = all_p[0].find('strong').text.strip()
        span_data['number of cases'] = all_p[1].find('strong').find('span').text.strip().split()[-1]
        span_data['number of released from Isolation'] = all_p[2].find('span').find('strong').text.strip().split()[-1]
        data.append(span_data)
else:
    print('no nav element found')

if data:
    field_names = data[0].keys()
    with open('data.csv', 'w', newline='') as outfile:
        dictwriter = csv.DictWriter(outfile, field_names)
        dictwriter.writeheader()
        dictwriter.writerows(data)