from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv


def write_data(datas):
    keys = datas[0].keys()
    with open('Coral_wholesale.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, keys)
        writer.writeheader()
        writer.writerows(datas)


# options = Options()
# options.add_argument("--start-maximized")
# options.add_argument('--headless')
driver = webdriver.Firefox()
url = 'https://www.google.com/maps/search/aquarium+store+usa/@36.2076441,-113.7413709,4z/data=!4m2!2m1!6e6?hl=en'
usa_url = 'https://www.google.com/maps/place/United+States/@36.2076441,-113.7413709,4z/data=!3m1!4b1!4m9!1m3!2m2!1saquarium+store+usa!6e6!3m4!1s0x54eab584e432360b:0x1c3bb99243deb742!8m2!3d39.7663253!4d-101.4038086?hl=en'
driver.get(url)
time.sleep(10)
element = driver.find_element_by_name('q')
element.clear()
element.send_keys(' Coral wholesale usa')
element.send_keys(Keys.RETURN)
time.sleep(10)
all_data = []


def query_page(driver):
    store_datas = []
    try:
        all_title = driver.find_elements_by_tag_name('h3')
    except NoSuchElementException:
        driver.quit()
        return store_datas

    for i in range(len(all_title)):
        try:
            title = all_title[i]
        except IndexError:
            driver.quit()

        ActionChains(driver).move_to_element(title).click(title).perform()
        time.sleep(5)
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
            store_description = driver.find_element_by_xpath(
                '//div[@class="section-editorial-quote"]/span').text
        except NoSuchElementException:
            store_description = None
        if store_description:
            store_data['store_description'] = store_description
        else:
            store_data['store_description'] = ''

        # store address
        try:
            store_address = driver.find_element_by_xpath(
                '//button[@data-tooltip="Copy address"]/div/div[2]/div').text
        except NoSuchElementException:
            store_address = None
        if store_address:
            store_data['store_address'] = store_address
        else:
            store_data['store_address'] = ''

        # store website
        try:
            store_website = driver.find_element_by_xpath(
                '//button[@data-tooltip="Open website"]/div/div[2]/div').text
        except NoSuchElementException:
            store_website = None
        if store_website:
            store_data['store_website'] = store_website
        else:
            store_data['store_website'] = ''

        # store phone
        try:
            store_phone = driver.find_element_by_xpath(
                '//button[@data-tooltip="Copy phone number"]').get_attribute('aria-label').split(':')[-1].strip()
        except NoSuchElementException:
            store_phone = None
        if store_phone:
            store_data['store_phone'] = store_phone
        else:
            store_data['store_phone'] = ''

        # store state
        try:
            store_state = driver.find_element_by_xpath(
                '//button[@data-tooltip="Copy plus code"]').get_attribute('aria-label')
            store_state = store_state.split(
                ':')[-1].strip().split(' ', maxsplit=1)[-1]
        except NoSuchElementException:
            store_state = None
        if store_state:
            store_data['store_state'] = store_state
        else:
            store_data['store_state'] = ''
        store_datas.append(store_data)

        time.sleep(5)
        try:
            back_btn = driver.find_element_by_xpath(
                '//button[@class="section-back-to-list-button blue-link noprint"]/span')
            ActionChains(driver).move_to_element(
                back_btn).click(back_btn).perform()
        except NoSuchElementException:
            driver.back()
        time.sleep(5)
        try:
            all_title = driver.find_elements_by_tag_name('h3')
            time.sleep(5)
        except NoSuchElementException:
            driver.quit()
            return store_datas
        except TimeoutException:
            driver.quit()
            return store_datas
    return store_datas

while True:
    datas = query_page(driver)
    all_data.extend(datas)

    # move to next page
    try:
        next_page = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@aria-label=" Next page "]'))
        )
    except:
        driver.quit()
        break
    if next_page:
        next_btn = driver.find_element_by_xpath(
            '//button[@aria-label=" Next page "]')
        ActionChains(driver).move_to_element(
            next_btn).click(next_btn).perform()
        time.sleep(10)


write_data(all_data)
print('Done')
