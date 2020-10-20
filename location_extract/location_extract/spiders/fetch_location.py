import scrapy
import pandas as pd
import os

class LocationSpider(scrapy.Spider):
    name = "state_location"
    df = pd.read_csv('Spacy Dataset.csv')
    vals = df['University'].tolist()
    #print(len(vals),"***********")
    # vals = ["srtmu","batu","West Bengal university of technology","Savitribai Phule Pune University"]
    vals = ["srtmu","srtmu"]
    start_urls = [
        'https://www.google.com/search?q='+val for val in vals
    ]
    def parse(self, response):
        # print('---------------------------------------', response.text, "888888888")
        university_name = response.xpath("//div[contains(@class,'BNeawe deIvCb AP7Wnd')]/text()").get()
        location = response.xpath("//div[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()").get()
        location = location.replace("\n", "")
        file_path = "output.csv"
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['university_name', 'location'])
            df.to_csv('output.csv')
            print("File Created Successfully...!")
        df = pd.read_csv('output.csv', index_col=[0])
        if len(university_name)> 1 and len(location)> 1:
            df = df.append(pd.Series([university_name, location], index=df.columns), ignore_index=True)
        else:
            df = df.append(pd.Series(['data_not_found', 'data_not_found'], index=df.columns), ignore_index=True)
        df.to_csv('output.csv')
        yield {'university_name':university_name,'location': location}
