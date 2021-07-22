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
        
        athletes[i["name"]][year][tag]["rank"]      = i["rank"]        
        athletes[i["name"]][year][tag]["Time"]      = i["total"]
        athletes[i["name"]][year][tag]["1000"]      = i["1000"]
        athletes[i["name"]][year][tag]["2000"]      = i["2000"]
        athletes[i["name"]][year][tag]["1000-2000"] = i["1000-2000"]
        athletes[i["name"]][year][tag]["2000-3000"] = i["2000-3000"]
        athletes[i["name"]][year][tag]["Speed"]     = i["speed"]
        
df = pd.read_csv("2020/Qualif.csv", sep=",")
add_data(df, "qualif", "2020")
df = pd.read_csv("2020/Final.csv", sep=",")
add_data(df, "final", "2020")


df = pd.read_csv("2019/Qualif.csv", sep=",")
add_data(df, "qualif", "2019")
df = pd.read_csv("2019/Final.csv", sep=",")
add_data(df, "final", "2019")


with open("women_individual_pursuit.json", "w") as f:
    f.write(json.dumps(athletes, indent=True, skipkeys=True))
    
    