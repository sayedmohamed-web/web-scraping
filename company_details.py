import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = 'https://belilokal.thestar.com.my/shop.aspx'

page = requests.get(base_url)
soup = BeautifulSoup(page.text, 'html.parse')
urls = soup.find_all(class_='red submit-link more-info-btn')
all_urls = []
for url in urls:
    all_urls.append(urljoin(base_url, url['href']))
print(all_urls)