from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import random
import csv

def get_page_detail(driver):
    time.sleep(random.choice(range(5, 10)))
    page_data = {}
    try:
        name = driver.find_element_by_tag_name('h1').text
        page_data['name'] = name
    except NoSuchElementException:
        page_data['name'] = ''
    
    try:
        ratings = driver.find_element_by_class_name('review-summary-wrapper--73f24').text.strip().split('(')[0]
        page_data['ratings'] = ratings
    except NoSuchElementException:
        page_data['ratings'] = ''

    try:    
        num_of_reviews = driver.find_element_by_class_name('reviewsCount--042fd').text.strip()[1:-1]
        page_data['num_of_reviews'] = num_of_reviews
    except NoSuchElementException:
        page_data['num_of_reviews'] = ''

    try:  
        address = driver.find_element_by_xpath('//p[@itemprop="address"]').get_attribute('content')
        page_data['address'] = address
    except NoSuchElementException:
        page_data['address'] = ''
    
    try:
        website = driver.find_element_by_xpath('//div[@class="website-call-buttons--281fc"]/div/span/a').get_attribute('href')
        page_data['website'] = website
    except NoSuchElementException:
        page_data['website'] = ''
    
    try:
        social_links = driver.find_element_by_class_name('socialLinks--16520')
        links = social_links.find_elements_by_class_name('link--1ea04')
        for link in links:
            if 'facebook' in link.find_element_by_tag_name('a').get_attribute('title'):
                page_data['facebook'] = link.find_element_by_tag_name('a').get_attribute('href')
            else:
                page_data['facebook'] = ''
            if 'instagram' in link.find_element_by_tag_name('a').get_attribute('title'):
                page_data['instagram'] = link.find_element_by_tag_name('a').get_attribute('href')
            else:
                page_data['instagram'] = ''
    except NoSuchElementException:
        pass
    return page_data


driver = webdriver.Chrome()
driver.get('https://www.theknot.com/marketplace/wedding-reception-venues-dallas-tx?distance=within-50-miles&price_range=inexpensive&sort=recommended')
time.sleep(random.choice(range(5, 10)))

radio = driver.find_element_by_name('distance-filters') 
radio.find_elements_by_class_name('label-text--13d6d')[3].click()
time.sleep(random.choice(range(5, 10)))

price = driver.find_element_by_name('price_range-filters') 
checkboxs = price.find_elements_by_xpath('.//span[@class="multiSelectLabel--083cb"]')
for checkbox in checkboxs:
    checkbox.click()
    time.sleep(random.choice(range(5, 10)))

all_data = []
while True:
    all_urls = []
    links = driver.find_elements_by_class_name('click-container--48a45')
    for link in links:
        all_urls.append(link.get_attribute('href'))

    visited = set()
    for i in range(len(all_urls)):
        link = random.choice(links)
        if link.get_attribute('href') in visited:
            continue
        visited.add(link.get_attribute('href'))
        home_page = driver.window_handles[0]
        link.click()
        new_window = driver.window_handles[1]
        driver.switch_to_window(new_window)
        time.sleep(random.choice(range(5, 10)))
        page_detail = get_page_detail(driver)
        print(page_detail)
        all_data.append(page_detail)
        driver.close()
        driver.switch_to_window(home_page)
        time.sleep(random.choice(range(5, 10)))
    try:
        next_page = driver.find_element_by_xpath('//a[@rel="next"]')
        if next_page:
            next_page.click()
            time.sleep(15)
    except:
        break
        
    

fields_name = all_data[0].keys()
with open('theknot.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fields_name)
    writer.writeheader()
    writer.writerows(all_data)
