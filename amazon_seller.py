from selenium import webdriver
import csv

url = 'https://www.amazon.com/gp/search/other/ref=sr_in_a_1?rh=i%3Aelectronics%2Cn%3A172282&page=2&pickerToList=brandtextbin&indexField=a&ie=UTF8&qid=1603562645'
driver = webdriver.Firefox()
driver.get(url)

all_links = []

uls = driver.find_elements_by_class_name('s-see-all-indexbar-column')
for ul in uls:
    for a in ul.find_elements_by_class_name('a-link-normal'):
        item_dict = {}
        name = a.get_attribute('title')
        url = a.get_attribute('href')
        item_dict['name'] = name
        item_dict['url'] = url
        all_links.append(item_dict)


keys = all_links[0].keys()
with open('amazon_seller_1.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(all_links)