from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv

usa_state = [
'Alabama','Alaska',
'Arizona',
'Arkansas',
'California',
'Colorado',
'Connecticut',
'Delaware',
'Florida',
'Georgia',
'Hawaii',
'Idaho',
'Illinois',
'Indiana',
'Iowa',
'Kansas',
'Kentucky',
'Louisiana',
'Maine',
'Maryland',
'Massachusetts',
'Michigan',
'Minnesota',
'Mississippi',
'Missouri',
'Montana',
'Nebraska',
'Nevada',
'New Hampshire',
'New Jersey',
'New Mexico',
'New York',
'North Carolina',
'North Dakota',
'Ohio',
'Oklahoma',
'Oregon',
'Pennsylvania',
'Rhode Island',
'South Carolina',
'South Dakota',
'Tennessee',
'Texas',
'Utah',
'Vermont',
'Virginia',
'Washington',
'West Virginia',
'Wisconsin',
'Wyoming']

def write_data(datas):
    keys = datas[0].keys()
    with open('Aquarium_wholesale.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, keys)
        writer.writeheader()
        writer.writerows(datas)

# srape store information
def get_store_details(driver):
    store_data = {}
    # store name
    try:
        store_name = driver.find_element_by_css_selector('h1 > span').text
    except NoSuchElementException:
        store_name = None
    if store_name:
        store_data['store_name'] = store_name
    else:
        store_data['store_name'] = ''
    # store description
    try:
        store_description = driver.find_element_by_xpath('//div[@class="section-editorial-quote"]/span').text
    except NoSuchElementException:
        store_description = None
    if store_description:
        store_data['store_description'] = store_description
    else:
        store_data['store_description'] = ''
        
    # store address
    try:
        store_address = driver.find_element_by_xpath('//button[@data-tooltip="Copy address"]/div/div[2]/div').text
    except NoSuchElementException:
        store_address = None
    if store_address:
        store_data['store_address'] = store_address
    else:
        store_data['store_address'] = ''
    # store website
    try:
        store_website = driver.find_element_by_xpath('//button[@data-tooltip="Open website"]/div/div[2]/div').text
    except NoSuchElementException:
        store_website = None
    if store_website:
        store_data['store_website'] = store_website
    else:
        store_data['store_website'] = ''
    # store phone
    try:
        store_phone = driver.find_element_by_xpath('//button[@data-tooltip="Copy phone number"]').get_attribute('aria-label').split(':')[-1].strip()
    except NoSuchElementException:
        store_phone = None
    if store_phone:
        store_data['store_phone'] = store_phone
    else:
        store_data['store_phone'] = ''
    # store state
    try:
        store_state = driver.find_element_by_xpath('//button[@data-tooltip="Copy plus code"]').get_attribute('aria-label')
        store_state = store_state.split(':')[-1].strip().split(' ', maxsplit=1)[-1]
    except NoSuchElementException:
        store_state = None
    if store_state:
        store_data['store_state'] = store_state
    else:
        store_data['store_state'] = ''
    
    try:
        back_btn = driver.find_element_by_xpath('//button[@class="section-back-to-list-button blue-link noprint"]')
        ActionChains(driver).move_to_element(back_btn).click(back_btn).perform()
    except NoSuchElementException:
        pass
    return store_data
    # end of get_store_details

def get_driver():
    url= 'https://www.google.com/maps/search/aquarium+store+usa/@31.6529987,-95.672194,4z/data=!3m1!4b1?hl=en'
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)
    
    return driver

def change_search_term(search_term, state_name):
    search = driver.find_element_by_name('q')
    search.clear()
    search.send_keys(search_term+' '+state_name + ' USA')
    search.send_keys(Keys.RETURN)
    driver.implicitly_wait(3)
    return driver

def get_page_detail(driver):
    all_data = []
    num_page_visited = 0
    try:
        search_results = driver.find_elements_by_class_name('section-result-text-content')
    except NoSuchElementException:
        return all_data
    while num_page_visited < len(search_results):
        store = search_results[num_page_visited]
        ActionChains(driver).move_to_element(store).click(store).perform()
        time.sleep(3)
        store_detail = get_store_details(driver)
        all_data.append(store_detail)
        num_page_visited += 1
        time.sleep(3)
        try:
            search_results = driver.find_elements_by_class_name('section-result-text-content')
        except NoSuchElementException:
            return all_data
    return all_data


all_store_data = []
driver = get_driver()
for state in usa_state:
    change_search_term('Aquarium wholesale', state)
    time.sleep(5)

    while True:
        try:
            page_data = get_page_detail(driver)
        except:
            pass
        if page_data:
            all_store_data.extend(page_data)
        try:
            next_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@id="n7lv7yjyC35__section-pagination-button-next"]')))
        except TimeoutException:
            break
        if next_btn is not None:
            ActionChains(driver).move_to_element(next_btn).click(next_btn).perform()
        else:
            break

write_data(all_store_data)
print('done')