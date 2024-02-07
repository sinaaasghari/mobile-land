from Scrapper import Scrapper
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd


if __name__ == '__main__':
    links = list()
    with open('links/kiarash-links.txt', 'r') as file:
        for row in file.readlines():
            links.append(row.replace('\n', ''))

    pool = ThreadPool(7)
    phone_details = pool.map(Scrapper.scrape_phone_data, links[:20])
    pool.close()
    pool.join()

    df = pd.DataFrame(phone_details)
    df.to_csv('test_data_with_multiThread_scrap.csv')

