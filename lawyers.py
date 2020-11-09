from selenium import webdriver


driver = webdriver.Firefox()
driver.get(
    'https://lawyers.findlaw.com/lawyer/practice/immigration-naturalization-law'
)
state_links = driver.find_element_by_xpath(
    '//*[text() = "Immigration Lawyers By State"]/parent::div')
urls = state_links.find_elements_by_xpath('.//li/a')
for url in urls:
    print(url.get_attribute('href'))

driver.get('https://lawyers.findlaw.com/lawyer/practicestate/immigration-naturalization-law/north-carolina')
all_cities = driver.find_elements_by_xpath('//li/a/b')
all_links = []
for city in all_cities:
    city.click()
    driver.implicitly_wait(5)
    links = driver.find_elements_by_xpath(
        '//div[@class="small-12 large-4 columns links"]/div/a')
    for link in links:
        all_links.append(
            {'city': link.text, 'city_url': link.get_attribute('href')}
        )


for city in all_links:
    city_name = city.get('city')
    print('city name = ')
