from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

url = 'https://experience.arcgis.com/experience/79cb51d21ecb4f58b3760192eace5428'
driver = webdriver.Firefox()
driver.get(url)
driver.implicitly_wait(60)

wait = WebDriverWait(driver, 60)
wait.until(EC.element_to_be_clickable(driver.find_element_by_class_name('ember-view')))
driver.find_element_by_class_name('ember-view').click()

full_data = driver.find_element_by_tag_name('full-container')
if full_data:
    data_items = driver.find_elements_by_tag_name('span')
    if data_items:
        data = []
        for data_item in data_items:
            item_dict = {}
            item_dict['city'] = data_item.find_element_by_xpath('//p/strong').text
            item_dict['cases'] = data_item.find_element_by_xpath('//p/strong/span').text
            item_dict['released'] = data_item.find_element_by_xpath('//p/span/strong').text
            data.append(item_dict)

if data:
    field_names = data[0].keys()
    with open('data.csv', 'w', newline='') as outfile:
        dictwriter = csv.DictWriter(outfile, field_names)
        dictwriter.writeheader()
        dictwriter.writerows()