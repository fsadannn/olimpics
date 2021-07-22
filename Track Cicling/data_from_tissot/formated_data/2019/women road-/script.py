# rank,num,name,time
import pandas as pd
import json
import re

athletes = {}

def fix_quotes(string):
    return string
    # return re.sub("(\w+):", r'"\1":', string)
    

def add_data(df,tag, year = "2019"):
    for idx, i in df.iterrows():
        if not 'name' in list(df.columns):
            # print('here')
            continue
        if not i["name"] in athletes:
            athletes[i["name"]] = {}
        # athletes[i["name"]]["Country"] = i["country"]
        athletes[i["name"]][year] = {}
        athletes[i["name"]][year][tag] = {}
        
        athletes[i["name"]][year][tag]["rank"]    = str(i["rank"])       
        athletes[i["name"]][year][tag]["Time"]    = str(i["time"])       

df = pd.read_csv("2020/final.csv", sep=",")
add_data(df, "road_race", "2020")

df = pd.read_csv("2019/final.csv", sep=",")
add_data(df, "road_race", "2019")


with open("women_road_race.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    