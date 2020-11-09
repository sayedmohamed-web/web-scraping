from selenium import webdriver
from bs4 import BeautifulSoup
import csv


driver = webdriver.Firefox()
driver.get('https://www.google.com/maps/search/wholesale+seafood+buyers+LA/@33.9908775,-118.5920356,10z/data=!3m1!4b1?hl=en')
driver.implicitly_wait(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
results = soup.find_all(class_='section-result')
all_data = []
for result in results:
	data  = {}
	title = location = phone_number = website = ''
	title = result.find('h3').get_text()
	location = result.find('span', class_='section-result-location').get_text()
	phone_number = result.find('span', class_='section-result-info section-result-phone-number').get_text().strip()
	website = result.find('a', class_='section-result-action section-result-action-wide')
	if website:
		website = website['href']
	else:
		website = ''
	data['title'] = title
	data['location'] = location
	data['phone_number'] = phone_number
	data['website'] = website
	all_data.append(data)

fieldsname = all_data[0].keys()
with open('seafood.csv', 'w', newline='') as outfile:
	writer = csv.DictWriter(outfile, fieldsname)
	writer.writeheader()
	writer.writerows(all_data)