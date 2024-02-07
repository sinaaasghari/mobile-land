from Scrapper import Scrapper
import pandas as pd

if __name__ == '__main__':
    file = open('kiarash-links.txt', 'r')
    links = str.split(file.read(), '\n')
    phones_data = []
    for i in range(20):
        phones_data.append(Scrapper.scrape_phone_data(links[i]))
    df = pd.DataFrame(phones_data)
    df.to_csv('test_data.csv')
    file.close()
