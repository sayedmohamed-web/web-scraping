import requests
from bs4 import BeautifulSoup
import csv
import time


# home_page = requests.get('https://antiquetrail.com/')
# soup = BeautifulSoup(home_page.text, 'html.parser')
# all_states = soup.find_all('div', id='all-states-menu')
# for a in all_states.find_all('a', href=True):
#     continue

store_details = []

soup = BeautifulSoup(requests.get('http://www.alabamaantiquetrail.com/').text, 'html.parser')
all_stores = soup.find_all('div', style='width: 49%; margin-bottom: 6px;')[1:]
for store in all_stores:
    store_info = {}
    div = store.find('div', style='font-family:Arial; font-size: 10pt; padding: 0px 0px 5px 8px;')
    name = div.find('div').find('a').find('strong').text
    website = div.find('div').find('a')['href']
    phone = div.find('div', style='font-family:Arial; font-size: 14px; padding: 0px 0px 5px 0px;').find('a').text
    address = div.find('div', style='font-family:Arial; font-size: 12px;').text.strip().split()
    address = ' '.join([addr for addr in address])
    store_info['name'] = name
    store_info['website'] = website
    store_info['phone'] = phone
    store_info['address'] = address
    store_details.append(store_info)

keys = store_details[0].keys()
with open('store.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(store_details)
