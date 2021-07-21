import pandas as pd
import json
import re

athletes = {}

def fix_quotes(string):
    return re.sub("(\w+):", r'"\1":', string)
    
def add_data_scratch(df,tag, year = "2019"):
    for idx, i in df.iterrows():
        if not 'name' in list(df.columns):
            # print('here')
            continue
        if not i["name"] in athletes:
            athletes[i["name"]] = {}
            athletes[i["name"]]["Country"] = i["country"]
            athletes[i["name"]][year] = {}
        if not year in athletes[i["name"]]:
            athletes[i["name"]][year] = {}
            
        athletes[i["name"]][year][tag] = {}
        athletes[i["name"]][year][tag]["rank"]    = str(i["rank"])   
          
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
        
        athletes[i["name"]][year][tag]["rank"]    = i["rank"]        
        athletes[i["name"]][year][tag]["sprints_won"]    = str(i["sprints"])
        athletes[i["name"]][year][tag]["finish_order"]     = str(i["order"])
        athletes[i["name"]][year][tag]["balance"] = str(i["balance"])
        athletes[i["name"]][year][tag]["total_points"]   = str(i["total"])

df = pd.read_csv("2019/Scratch.csv", sep=",")
add_data_scratch(df, "scratch", "2019")
df = pd.read_csv("2020/Scratch.csv", sep=",")
add_data_scratch(df, "scratch", "2020")

df = pd.read_csv("2019/Elimination.csv", sep=",")
add_data_scratch(df, "elimination", "2019")
df = pd.read_csv("2020/Elimination.csv", sep=",")
add_data_scratch(df, "elimination", "2020")

df = pd.read_csv("2019/time.csv", sep=",")
add_data(df, "time", "2019")
df = pd.read_csv("2020/Time.csv", sep=",")
add_data(df, "time", "2020")


with open("women_omnium.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    