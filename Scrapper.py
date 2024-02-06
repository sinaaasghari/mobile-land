import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import logging


class Scrapper:
    _brands_to_search = ['alcatel', 'Apple', 'Asus', 'BLU', 'HTC', 'Huawei', 'Infinix', 'Lenovo', 'LG', 'Nokia', 'Sony',
                         'Xiaomi', 'ZTE', 'Samsung']
    _first_page_url = 'https://www.gsmarena.com/makers.php3'

    @staticmethod
    def get_soup(url):
        try:
            time.sleep(np.random.rand() / 100)
            headers = {'user-agent': 'Chrome/58.0.3029.110', 'accept-language': 'en-US'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            logging.error(f"Failed to request to {url} {str(e)}")

    @staticmethod
    def get_brand_base_urls():
        soup = Scrapper.get_soup(Scrapper._first_page_url)
        brand_base_urls = []
        for row in soup.select('.st-text')[0].find_all('td'):
            for brand in Scrapper._brands_to_search:
                if brand in row.find('a').text:
                    brand_base_urls.append('https://www.gsmarena.com/' + row.find('a')['href'])

        # there are two names that contains sony or asus that we don't want to work with.
        brand_base_urls.remove('https://www.gsmarena.com/garmin_asus-phones-65.php')
        brand_base_urls.remove('https://www.gsmarena.com/sony_ericsson-phones-19.php')
        return brand_base_urls

    # returns the links of all pages from all brands
    @staticmethod
    def get_page_urls(brand_base_urls):
        page_urls = []
        for url in brand_base_urls:
            soup = Scrapper.get_soup(url)
            try:
                max_num_page = int(soup.select('.nav-pages')[0].find_all('a')[3].text)
            except:
                max_num_page = int(soup.select('.nav-pages')[0].find_all('a')[2].text)
            first_sec, second_sec = url.split('-phones-')
            for num in range(1, max_num_page + 1):
                page_urls.append(first_sec + '-phones-f-' + second_sec.split('.')[0] +
                                 '-0-p' + '{}'.format(num) + '.' +
                                 second_sec.split('.')[1])
        return page_urls

    @staticmethod
    def get_phone_urls(page_url):
        phone_urls = []
        for url in page_url:
            soup = Scrapper.get_soup(url)
            for phone in soup.select('.makers')[0].find_all('li'):
                phone_urls.append('https://www.gsmarena.com/' + phone.find('a')['href'])
        pass

    @staticmethod
    def scrape_phone_data(phone_url):
        # TODO
        pass
