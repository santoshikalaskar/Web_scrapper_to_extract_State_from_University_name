import requests
import pandas as pd
from lxml import html
import re, os

final_list = []
univer_list = []
df1 = pd.read_csv('Spacy Dataset.csv')
file_path = "output.csv"
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['University','university_name', 'State_location','State'])
    df.to_csv('output.csv')
    print("File Created Successfully...!")
df = pd.read_csv('output.csv', index_col=[0])
for _, itr in df1[301:400].iterrows():
    Uni_vals = itr['University']

    if str(Uni_vals) != 'nan':
        page = requests.get("https://www.google.com/search?q="+str(Uni_vals))
        tree = html.fromstring(page.content)
        University_name = tree.xpath("//div[contains(@class,'BNeawe deIvCb AP7Wnd')]/text()")
        if University_name == None:
            University_name = tree.xpath("//div[contains(@class,'BNeawe vvjwJb AP7Wnd')]/text()")
        try:
            State_location = tree.xpath("//div[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()").replace("\n", "")

        except:
            State_location = tree.xpath("//div[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()")
            # State_location = tree.xpath("//span[contains(@class,'BNeawe tAd8D AP7Wnd')]/text()")
        try:
            State_location = State_location[0]
        except:
            State_location = State_location

        State =''

        try:
            # print(Uni_vals,State_location)
            string_check = re.compile('[,]')
            print(State_location,"000000000000")
            if (string_check.search(State_location) == None):
                print("******", str(State_location).strip())
                if re.search('in', str(State_location).strip()):
                    State = State_location.split('in')[-1].strip()
                    print("********", State)
                else:
                    if 'day ago' in State_location or 'Times Now' in State_location:
                        State = 'State_not_found'
                        print("77777")
            else:
                State = State_location.split(',')[-1]
                # State = State.rsplit(' ', 1)[0]

            final_list.append(State.strip())
            print("11111",Uni_vals,"---------",University_name,"------", State_location,"-------", State)
            df = df.append(pd.Series([Uni_vals,University_name, State_location, State], index=df.columns), ignore_index=True)
        except:
            State ="State_not_found"
            final_list.append(State)
            print("2222",Uni_vals, "---------", University_name, "------", State_location, "-------", State)
            df = df.append(pd.Series([Uni_vals,University_name,State_location, State], index=df.columns), ignore_index=True)
    else:
        print("11")
        State = ""
        final_list.append('')
        print('none', "---------", 'none', "------", 'none', "-------", 'none')
        df = df.append(pd.Series(['','', '', ''], index=df.columns), ignore_index=True)
    df.to_csv('output.csv')
print("------------")

# print(final_list)


