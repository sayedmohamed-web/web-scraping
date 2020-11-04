from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time


def write_csv(data):
    keys = data[0].keys()
    with open('outfile.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, keys)
        writer.writeheader()
        writer.writerows(data)

# handle the presence of multiple phone number and check that for other fields
def get_camp_data(camp_div):
    camp_data = {}
    camp_data['name'] = camp_div.find('strong').get_text().strip()
    address = camp_div.find(class_='col-sm-4 ng-binding').get_text().strip().split('\n')
    camp_data['address'] = ' '.join([addre.strip() for addre in address])
    camp_data['telephone'] = camp_div.find('a', attrs={'class':'ng-binding'})['href'].split(':')[-1]
    return camp_data

def get_camp_page_data(soup):
    page_data = []
    all_divs = soup.find_all(class_='col-sm-12 int-table ng-scope')
    for div in all_divs:
        page_data.append(get_camp_data(div))
    return page_data


if __name__ == '__main__':
    all_data = []
    driver = webdriver.Chrome()
    driver.get('https://www.rvusa.com/rv-parks-campgrounds/California-6')
    time.sleep(5)
    while True:
        try:
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            data = get_camp_page_data(soup)
            all_data.extend(data)
            next_page = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Next'))
            )
            if driver.find_element_by_partial_link_text('Next').get_attribute('class') == 'inactive':
                driver.quit()
                break
            next_page.click()
        except TimeoutException:
            driver.quit()
            break
    
    write_csv(all_data)