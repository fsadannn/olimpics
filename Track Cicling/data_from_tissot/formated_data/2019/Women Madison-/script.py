import pandas as pd
import json
import re

athletes = {}

def fix_quotes(string):
    return string
    # return re.sub("(\w+):", r'"\1":', string)
    

def add_data(df,tag, year = "2019"):
    for idx, i in df.iterrows():
        names = ["Name Black","Name red"]    
        for name in names:
            if not name in list(df.columns):
                # print('here')
                continue
            if not i[name] in athletes:
                athletes[i[name]] = {}
            athletes[i[name]]["Country"] = i["Country"]
            athletes[i[name]][year] = {}
            athletes[i[name]][year][tag] = {}

            athletes[i[name]][year][tag]["rank"]    = i["Rank"]        
            for num in range(1,13):
                athletes[i[name]][year][tag][str(num)]  = i[str(num)]        
            athletes[i[name]][year][tag]["balance"]    = str(i["Lap Balance"])
            athletes[i[name]][year][tag]["finish_order"]   = str(i["Finish Order"])
            athletes[i[name]][year][tag]["points"]   = str(i["Points"])

df = pd.read_csv("2020/madison.csv", sep=",")
add_data(df, "madison", "2020")

df = pd.read_csv("2019/madison.csv", sep=",")
add_data(df, "madison", "2019")


with open("women_madison.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    