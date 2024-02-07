from Scrapper import Scrapper
import pandas as pd
from threading import Thread
from time import sleep


if __name__ == '__main__':
    file = open('kiarash-links.txt', 'r')
    links = str.split(file.read(), '\n')
    phones_data = []
    for i in range(20):
        
        like_name = links[i][24:]
        print(f' initialing {like_name}')
        
        t = Thread(target=Scrapper.scrape_phone_data , args=(links[i] , phones_data) , name=like_name)
        t.start()
        
        sleep(2)
        
    df = pd.DataFrame(phones_data)
    df.to_csv('test_data.csv')
    file.close()
