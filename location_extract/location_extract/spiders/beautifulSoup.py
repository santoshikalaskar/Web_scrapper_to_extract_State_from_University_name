import requests
import pandas as pd
from lxml import html
import re

final_list = []

df = pd.read_csv('Spacy Dataset.csv')
for _, itr in df[0:5].iterrows():
    Uni_vals = itr['University']

    if str(Uni_vals) != 'nan':
        page = requests.get("https://www.google.com/search?q="+str(Uni_vals))
        tree = html.fromstring(page.content)
        University_name = tree.xpath("//div[contains(@class,'BNeawe deIvCb AP7Wnd')]/text()")
        if University_name == None:
            University_name = tree.xpath("//div[contains(@class,'BNeawe vvjwJb AP7Wnd')]/text()")
        State_location = tree.xpath("//div[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()")
        try:
            State_location = State_location.replace("\n", "")
        except:
            State_location = tree.xpath("//span[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()")
        try:
            State_location = State_location[0]
        except:
            State_location = State_location

        State =''
        try:
            print(Uni_vals,State_location)
            string_check = re.compile('[,]')
            if (string_check.search(State_location) == None):
                if re.search('in', State_location):
                    State = State_location.split('in')[-1]
                    State = State.rsplit(' ', 1)[0]
                else:
                    State = State_location.rsplit(' ', 1)[0]
            else:
                State = State_location.split(',')[-1]
                State = State.rsplit(' ', 1)[0]

            final_list.append(State.strip())
        except:
            State ="State_not_found"
            final_list.append(State)
    else:
        print("11")
        State = ""
        final_list.append('')
print("------------")
print(final_list)


