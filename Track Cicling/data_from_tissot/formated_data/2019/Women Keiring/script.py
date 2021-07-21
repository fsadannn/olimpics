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
        
        athletes[i["name"]][year][tag]["rank"]    = i["rank"]        
        athletes[i["name"]][year][tag]["heat"]    = i["heat"]        
        athletes[i["name"]][year][tag]["Time"]    = str(i["time"])
        athletes[i["name"]][year][tag]["Speed"]   = str(i["speed"])

df = pd.read_csv("2020/first_round.csv", sep=",")
add_data(df, "first_round", "2020")
df = pd.read_csv("2020/quarter.csv", sep=",")
add_data(df, "quarter", "2020")
df = pd.read_csv("2020/semi.csv", sep=",")
add_data(df, "semi", "2020")
df = pd.read_csv("2020/final.csv", sep=",")
add_data(df, "final", "2020")


df = pd.read_csv("2019/first_round.csv", sep=",")
add_data(df, "first_round", "2019")
df = pd.read_csv("2019/first_round_repechage.csv", sep=",")
add_data(df, "first_round_repechage", "2019")
df = pd.read_csv("2019/quarter.csv", sep=",")
add_data(df, "quarter", "2019")
df = pd.read_csv("2019/semi.csv", sep=",")
add_data(df, "semi", "2019")
df = pd.read_csv("2019/final.csv", sep=",")
add_data(df, "final", "2019")


with open("women_time_trial.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    