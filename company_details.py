import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv
import random

base_url = 'https://belilokal.thestar.com.my/shop.aspx'


def random_time():
    return random.choice(range(1, 6))


def has_class(css_class):
    return css_class == 'red submit-link more-info-btn' or css_class == 'white read-story-btn'


def write_csv(dict_data):
    field_names = dict_data[0].keys()
    with open('company_details2.csv', 'w', newline='') as outfile:
        dict_writer = csv.DictWriter(outfile, field_names)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def get_urls(main_page_content):
    urls = []
    soup = BeautifulSoup(main_page_content, 'html.parser')
    all_urls = soup.find_all(class_=has_class)
    for page_url in all_urls:
        urls.append(urljoin(base_url, page_url['href']))
    return urls


def company_detail(company_url):
    company_data = {}
    page = requests.get(company_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    detail_div = soup.find(class_='desc-brand')
    title = detail_div.find('h2').find('span', attrs={'id': 'ContentPlaceHolder1_ItemTitle'}).get_text()
    if title:
        company_data['title'] = title
    description = detail_div.find(class_='scroll-info').find(
        'p', attrs={'id': 'ContentPlaceHolder1_ItemDescription'}).get_text()
    if description:
        company_data['description'] = description
    phone_number = detail_div.find('span', attrs={'id': 'ContentPlaceHolder1_ItemContact'}).get_text()
    if phone_number:
        company_data['phone number'] = phone_number
    services_area = detail_div.find('span', attrs={'id': 'ContentPlaceHolder1_ItemArea'}).get_text()
    if services_area:
        company_data['services ares'] = services_area
    address = detail_div.find('span', attrs={'id': 'ContentPlaceHolder1_ItemAddress'}).get_text()
    if address:
        company_data['address'] = address

    return company_data


driver = webdriver.Firefox()
data = []

driver.get(base_url)
time.sleep(random_time())
company_urls = get_urls(driver.page_source)
for url in company_urls:
    data.append(company_detail(url))

try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_rptPaging_nextbtnPage')))
except:
    driver.quit()

next_button = driver.find_element_by_id('ContentPlaceHolder1_rptPaging_nextbtnPage')

while next_button:
        next_button.click()
        time.sleep(random_time())
        company_urls = get_urls(driver.page_source)
        for url in company_urls:
            data.append(company_detail(url))
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_rptPaging_nextbtnPage')))
        except:
            driver.quit()
            break
        next_button = driver.find_element_by_id('ContentPlaceHolder1_rptPaging_nextbtnPage')

write_csv(data)