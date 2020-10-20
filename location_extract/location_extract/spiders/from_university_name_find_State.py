import scrapy
import pandas as pd
import os

class LocationSpider(scrapy.Spider):
    name = "state_location2"

    def start_requests(self):
        df = pd.read_csv('University_Dataset.csv')
        vals = df['University'].tolist()
        # vals = ["srtmu", "srtmu"]
        for val in vals:
            yield scrapy.Request(url="https://www.google.com/search?q="+val, dont_filter=True)

    def parse(self, response):
        # print('---------------------------------------', response.text, "888888888")
        Search_for = response.xpath("//title/text()").get()
        Search_for = Search_for.split(' - ')[0]
        University_name = response.xpath("//div[contains(@class,'BNeawe deIvCb AP7Wnd')]/text()").get()
        State_location = response.xpath("//div[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()").get()
        State_location = State_location.replace("\n", "")

        file_path = "State_output.csv"
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['Search_for','University_name', 'State_location'])
            df.to_csv('State_output.csv')
            print("File Created Successfully...!")
        df = pd.read_csv('State_output1.csv', index_col=[0])
        if len(University_name)> 1 and len(State_location)> 1 and len(Search_for)>1:
            df = df.append(pd.Series([Search_for,University_name, State_location], index=df.columns), ignore_index=True)
        else:
            df = df.append(pd.Series(['data_not_found','data_not_found', 'data_not_found'], index=df.columns), ignore_index=True)
        df.to_csv('State_output.csv')
        yield {'Search_for ':Search_for,'University_name':University_name,'State_location': State_location}
