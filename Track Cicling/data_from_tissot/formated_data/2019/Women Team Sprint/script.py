import pandas as pd
import json
import re

athletes = {}

def fix_quotes(string):
    return string
    # return re.sub("(\w+):", r'"\1":', string)
    

def add_data(df,tag, year = "2019"):
    for idx, i in df.iterrows():
        names = ["Athlete 1","Athlete 2"]    
        for index, name in enumerate(names):
            if not name in list(df.columns):
                # print('here')
                continue
            if not i[name] in athletes:
                athletes[i[name]] = {}
            athletes[i[name]]["Country"] = i["Country"]
            athletes[i[name]][year] = {}
            athletes[i[name]][year][tag] = {}
            
            if 'Heat' in i:
                athletes[i[name]][year][tag]["heat"]         = i["Heat"]            
                
            athletes[i[name]][year][tag]["rank"]            = i["rank"]        
            athletes[i[name]][year][tag]["race_order"]      = index        
            athletes[i[name]][year][tag]["lap_1"]           = str(i["Lap 1"])
            athletes[i[name]][year][tag]["lap_2"]           = str(i["Lap 2"])
            athletes[i[name]][year][tag]["total"]           = str(i["Total"])
            athletes[i[name]][year][tag]["speed"]           = str(i["Speed"])

df = pd.read_csv("2020/final.csv", sep=",")
add_data(df, "final", "2020")
df = pd.read_csv("2020/First_round.csv", sep=",")
add_data(df, "first_round", "2020")
df = pd.read_csv("2020/qualif.csv", sep=",")
add_data(df, "qualif", "2020")

df = pd.read_csv("2019/final.csv", sep=",")
add_data(df, "final", "2019")
df = pd.read_csv("2019/First_round.csv", sep=",")
add_data(df, "first_round", "2019")
df = pd.read_csv("2019/qualif.csv", sep=",")
add_data(df, "qualif", "2019")


with open("women_team_pursuit.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    