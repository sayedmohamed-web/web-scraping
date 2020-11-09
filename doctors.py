from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv


options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get('https://www.healthgrades.com/usearch?what=Dentistry&entityCode=PS328&searchType=PracticingSpecialty&where=New%20York%2C%20NY&pt=40.6638%2C%20-73.938141&pageNum=2&sort.provider=bestmatch')
driver.implicitly_wait(30) # seconds

all_doctor = []

for doctor in driver.find_elements_by_xpath('//li[@class="card-deck__standCard"]'):

    doctor_info = {}

    doctor_info['name'] = doctor.find_element_by_xpath('.//h3/a').text
    doctor_info['url'] = doctor.find_element_by_xpath('.//h3/a').get_attribute('href')
    doctor_info['specialty'] = doctor.find_element_by_xpath('.//div[@aria-label="Specialty:"]').text
    try:
        reviews_rating = doctor.find_element_by_xpath(
            './/div[@class="reviews-rating"]').get_attribute('aria-label')
        doctor_info['review_ratings'] = reviews_rating
    except:
        doctor_info['review_ratings'] = 'No Review Yet'
    doctor_info['number_of_reviews'] = doctor.find_element_by_xpath(
        './/span[@class="reviews-rating__reviews-text"]').get_attribute('aria-label')
    address = doctor.find_elements_by_xpath('.//div[@class="location-info__office-loc"]/span')
    if len(address) > 1:
        for index, addr in enumerate(address):
            key = 'address [%s]' % str(index+1)
            doctor_info[key] = addr.text
    else:
        doctor_info['address'] = doctor.find_element_by_xpath('.//div[@class="location-info__office-loc"]/span').text
    # doctor_info['phone'] = doctor.find_element_by_class_name('booking-options__booking-phone').text

    all_doctor.append(doctor_info)

if all_doctor:
    field_names = all_doctor[0].keys()
    with open('doctors2.csv', 'w', newline='') as outfile:
        dictwriter = csv.DictWriter(outfile, field_names)
        dictwriter.writeheader()
        dictwriter.writerows(all_doctor)
else:
    print('sorry, do not scrape nothing')