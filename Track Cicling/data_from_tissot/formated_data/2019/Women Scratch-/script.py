import pandas as pd
import json
import re

athletes = {}

def fix_quotes(string):
    return re.sub("(\w+):", r'"\1":', string)
    

def add_data(df,tag, year = "2019"):
    for idx, i in df.iterrows():
        if not 'name' in list(df.columns):
            # print('here')
            continue
        if not i["name"] in athletes:
            athletes[i["name"]] = {}
        athletes[i["name"]]["Country"] = i["country"]
        athletes[i["name"]][year] = {}
        athletes[i["name"]][year][tag] = {}
        
        athletes[i["name"]][year][tag]["rank"]    = str(i["rank"])       

df = pd.read_csv("2020/scratch.csv", sep=",")
add_data(df, "scratch", "2020")

df = pd.read_csv("2019/scratch.csv", sep=",")
add_data(df, "scratch", "2019")


with open("women_scratch.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    