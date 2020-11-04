from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import csv


options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://www.escpalumni.org/gene/main.php?langue=uk&base=520')
time.sleep(5)
driver.find_element_by_id('tarteaucitronPersonalize').click()
# ActionChains(driver).move_to_element(
#     search_button).click(search_button).perform()
time.sleep(5)
search_button = driver.find_element_by_class_name('bt-big').click()

all_urls = []
urls = driver.find_elements_by_css_selector('div.single_libel > a')
for url in urls:
    user = {}
    name = url.text
    profile_url = url.get_attribute('href')
    if name and profile_url:
        user['name'] = name
        user['profile_url'] = profile_url
        all_urls.append(user)

time.sleep(5)

for i in range(1000):
    try:
        time.sleep(5)
        next_button = driver.find_element_by_class_name('next').click()
        # ActionChains(driver).move_to_element(
        #     next_button).click(next_button).perform()
        urls = driver.find_elements_by_css_selector('div.single_libel > a')
        for url in urls:
            user = {}
            name = url.text
            print(name)
            profile_url = url.get_attribute('href')
            print(profile_url)
            if name and profile_url:
                user['name'] = name
                user['profile_url'] = profile_url
                all_urls.append(user)

        time.sleep(5)
    except NoSuchElementException:
        driver.quit()
        break
    except TimeoutException:
        driver.quit()
        break
    if i % 90 == 0:
        driver.implicitly_wait(60)

time.sleep(5)
keys = all_urls[7].keys()
with open('all_urls3.csv', 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(all_urls)
