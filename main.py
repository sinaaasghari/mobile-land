from Scrapper import Scrapper

if __name__ == '__main__':
    s24_data = Scrapper.scrape_phone_data('https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php')
    print(s24_data)