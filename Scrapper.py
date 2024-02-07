import numpy as np
from bs4 import BeautifulSoup
import requests
import time
import logging
import re


class Scrapper:
    _brands_to_search = ['alcatel', 'Apple', 'Asus', 'BLU', 'HTC', 'Huawei', 'Infinix', 'Lenovo', 'LG', 'Nokia', 'Sony',
                         'Xiaomi', 'ZTE', 'Samsung']
    _first_page_url = 'https://www.gsmarena.com/makers.php3'
    _failed_request_urls = []
    _core_dict = {'Octa': 8, 'Dual': 2, 'Quad': 4, 'Hexa': 6, 'Deca': 10}
    _sim_list = ['Micro-SIM', 'Nano-SIM', 'Mini-SIM']

    @staticmethod
    def get_soup(url):
        try:
            time.sleep(np.random.rand() / 100)
            headers = {'user-agent': 'Chrome/58.0.3029.110', 'accept-language': 'en-US'}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            Scrapper._failed_request_urls.append(url)
            logging.error(f'Failed to request to {url} {str(e)}')

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
        # will return phone_data dict from one phone page url
        # if phone is made before 2010 it will return None
        soup = Scrapper.get_soup(phone_url)
        headers = [row.text for row in soup.select('#specs-list')[0].find_all('th')]
        year = Scrapper.extract_year(soup, headers)
        if year < 2010:
            return None
        phone_data = {'year': year}
        Scrapper.extract_info(soup, headers, phone_data)
        return phone_data

    @staticmethod
    def extract_year(soup, headers):
        try:
            launch = headers.index('Launch')
        except:
            logging.error(f'could not find Launch as a header')
            return 0
        year_data = soup.select('#specs-list')[0].find_all('table')[launch].find(class_='nfo').text
        return int(re.findall(r'\d+', year_data)[0])

    @staticmethod
    def extract_info(soup, headers, phone_data):
        Scrapper.extract_basic_info(soup, phone_data)
        Scrapper.extract_platform_info(soup, headers, phone_data)
        Scrapper.extract_memory_info(soup, headers, phone_data)
        Scrapper.extract_network_info(soup, headers, phone_data)
        Scrapper.extract_sensor_info(soup, headers, phone_data)
        Scrapper.extract_body_info(soup, headers, phone_data)
        Scrapper.extract_display_info(soup, headers, phone_data)
        Scrapper.extract_price_info(soup, headers, phone_data)
        Scrapper.extract_battery_info(soup, headers, phone_data)

    @staticmethod
    def extract_basic_info(soup, phone_data):
        phone_data['name'] = ' '.join(soup.select('.specs-phone-name-title')[0].text.split(' ')[1:])
        phone_data['brand'] = soup.select('.specs-phone-name-title')[0].text.split(' ')[0]

    @staticmethod
    def extract_platform_info(soup, headers, phone_data):
        try:
            platform = headers.index('Platform')
            platform_info = [row.text for row in
                             soup.select('#specs-list')[0].find_all('table')[platform].find_all('td')]
            try:
                os_index = platform_info.index('OS') + 1
            except:
                os_index = -1
            try:
                core_index = platform_info.index('CPU') + 1
            except:
                core_index = -1
            if core_index != -1:
                core = platform_info[core_index].split(' ')[0].split('-')[0]
                try:
                    phone_data['core'] = float(core)
                except:
                    phone_data['core'] = Scrapper._core_dict.get(core, '')
            else:
                phone_data['core'] = ''
            if os_index != -1:
                try:
                    type = platform_info[os_index].split(',')[0].split(' ')[0]
                    version = platform_info[os_index].split(',')[0].split(' ')[1]
                except:
                    try:
                        type = platform_info[os_index].split(',')[0].split('^')[0]
                        version = platform_info[os_index].split(',')[0].split('^')[1]
                    except:
                        type = platform_info[os_index].split(',')[0]
                        version = ''
                phone_data['type'] = type
                phone_data['version'] = version
            else:
                phone_data['type'] = ''
                phone_data['version'] = ''
        except:
            phone_data['type'] = ''
            phone_data['version'] = ''
            phone_data['core'] = ''

    @staticmethod
    def extract_memory_info(soup, headers, phone_data):
        try:
            memory = headers.index('Memory')
            memory_info = [row.text for row in soup.select('#specs-list')[0].find_all('table')[memory].find_all('td')]
            try:
                memory_index = memory_info.index('Internal') + 1
            except:
                memory_index = -1
            if memory_index != -1:
                memory = list()
                items = memory_info[memory_index].split(', ')
                for item in items:
                    hard_ram = item.split()[:2]
                    hard_ram = [n.strip('GB') for n in hard_ram]
                    hard_ram = [n.strip('T') for n in hard_ram]
                    hard_ram = [n.strip('M') for n in hard_ram]
                    memory.append(tuple(hard_ram))
                phone_data['memory'] = memory
            else:
                phone_data['memory'] = ''
        except:
            phone_data['memory'] = ''

    @staticmethod
    def extract_network_info(soup, headers, phone_data):
        try:
            network = headers.index('Network')
            two = '0'
            tree = '0'
            four = '0'
            for row in soup.select('#specs-list')[0].find_all('table')[network].find_all('td'):
                if '2G' in row.text:
                    two = '1'
                if '3G' in row.text:
                    tree = '1'
                if '4G' in row.text:
                    four = '1'
            phone_data['network'] = ''.join([four, tree, two])
        except:
            phone_data['network'] = '000'

    @staticmethod
    def extract_sensor_info(soup, headers, phone_data):
        try:
            features = headers.index('Features')
            sensors_str = soup.select('#specs-list')[0].find_all('table')[features].find_all(class_='nfo')[0].text
            sensors_list = list()
            items = sensors_str.split(',')
            for item in items:
                item = item.strip()
                if '(' in item:
                    item = item.split('(')[0]
                if ')' in item:
                    continue
                item = item.strip()
                sensors_list.append(item)
            phone_data['sensor'] = sensors_list
        except:
            phone_data['sensor'] = ''

    @staticmethod
    def extract_body_info(soup, headers, phone_data):
        try:
            body = headers.index('Body')
            body_info = [row.text for row in soup.select('#specs-list')[0].find_all('table')[body].find_all('td')]
            try:
                dimensions_index = body_info.index('Dimensions') + 1
            except:
                dimensions_index = -1
            try:
                weigth_index = body_info.index('Weight') + 1
            except:
                weigth_index = -1
            try:
                sim_index = body_info.index('SIM') + 1
            except:
                sim_index = -1
            try:
                phone_data['dimensions'] = body_info[dimensions_index].split(' mm')[0]
            except:
                phone_data['dimensions'] = ''
            try:
                phone_data['weight'] = body_info[weigth_index].split(' g')[0]
            except:
                phone_data['weight'] = ''
            try:
                for sim in Scrapper._sim_list:
                    if sim in body_info[sim_index]:
                        phone_data['sim'] = sim
                        break
            except:
                phone_data['sim'] = ''
        except:
            phone_data['dimensions'] = ''
            phone_data['weight'] = ''
            phone_data['sim'] = ''

    @staticmethod
    def extract_display_info(soup, headers, phone_data):
        try:
            display = headers.index('Display')
            display_info = [row.text for row in soup.select('#specs-list')[0].find_all('table')[display].find_all('td')]
            try:
                size = display_info.index('Size') + 1
            except:
                size = -1
            if size != -1:
                try:
                    phone_data['size'] = display_info[size].split()[0]
                except:
                    phone_data['size'] = ''
                try:
                    phone_data['screen_to_body_ratio'] = display_info[size].split('~')[1].split('%')[0]
                except:
                    phone_data['screen_to_body_ratio'] = ''
            else:
                phone_data['size'] = ''
                phone_data['screen_to_body_ratio'] = ''
            try:
                resolution = display_info.index('Resolution') + 1
            except:
                resolution = -1
            if resolution != -1:
                phone_data['resolution'] = display_info[resolution].split(' pixels')[0]
                try:
                    phone_data['ppi_density'] = display_info[resolution].split('~')[1].split(' ')[0]
                except:
                    phone_data['ppi_density'] = ''
            else:
                phone_data['resolution'] = ''
                phone_data['ppi_density'] = ''
        except:
            phone_data['size'] = ''
            phone_data['screen_to_body_ratio'] = ''
            phone_data['resolution'] = ''
            phone_data['ppi_density'] = ''

    @staticmethod
    def extract_price_info(soup, headers, phone_data):
        try:
            misc = headers.index('Misc')
            price_info = [row.text for row in soup.select('#specs-list')[0].find_all('table')[misc].find_all('td')]
            try:
                price_index = price_info.index('Price') + 1
            except:
                price_index = -1
            if price_index != -1:
                if 'Prices' in [i.text for i in soup.select('.article-info-meta-link')]:
                    try:
                        phone_data['price'] = price_info[price_index].split()[
                            price_info[price_index].split().index('£') + 1].replace(',', '')
                    except:
                        phone_data['price'] = ''
                else:
                    phone_data['price'] = re.findall(r'\d+', price_info[price_index])[0]
            else:
                phone_data['price'] = ''
        except:
            phone_data['price'] = ''

    @staticmethod
    def extract_battery_info(soup, headers, phone_data):
        try:
            battery  = headers.index('Battery')
            battery_info = [row.text for row in soup.select('#specs-list')[0].find_all('table')[battery].find_all('td')]
            try:
                battery_index = battery_info.index('Type') + 1
            except:
                battery_index = -1
            try:
                phone_data['battery'] = re.findall(r'\d+', battery_info[battery_index])[0]
            except:
                phone_data['battery'] = ''
        except:
            phone_data['battery'] = ''
