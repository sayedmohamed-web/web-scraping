from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv

options = Options()
options.add_argument('--headless')
assert options.headless
driver = webdriver.Chrome(options=options)
driver.get('https://cloud.withgoogle.com/partners/?regions=EMEA_REGION&products=GOOGLE_WORKSPACE_PRODUCT&sort-type=RELEVANCE')
try:
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name('iframe'))
    )
    driver.find_element_by_class_name('hats-close').click()

except:
    pass

driver.switch_to.default_content()
time.sleep(5)

while True:
    try:
        driver.find_element_by_id('load-more-cards-button').click()
        time.sleep(5)
    except:
        break

all_urls = [url.get_attribute('href') for url in driver.find_elements_by_class_name('card__box')]
data = []
for url in all_urls:
    driver.get(url)
    time.sleep(5)
    name = driver.find_element_by_class_name('detail-hero__logo').get_attribute('alt')
    address = driver.find_element_by_class_name('detail-links__link').get_attribute('href')
    data.append({name:address})
    time.sleep(5)

fieldnames = data[0].keys()
with open('googleurls.csv', 'w', newline='') as outfile:
    dictwriter = csv.DictWriter(outfile, fieldnames)
    dictwriter.writeheader()
    dictwriter.writerows(data)                         