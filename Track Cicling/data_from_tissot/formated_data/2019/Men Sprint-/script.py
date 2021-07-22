import pandas as pd
import json
import re

athletes = {}

def fix_quotes(string):
    return re.sub("(\w+):", r'"\1":', string)
    

def add_data(df,tag, year = "2019"):
    for idx, i in df.iterrows():
        if not 'name' in i:
            continue
        if not i["name"] in athletes:
            athletes[i["name"]] = {}
        athletes[i["name"]]["Country"] = i["country"]
        athletes[i["name"]][year] = {}
        athletes[i["name"]][year][tag] = {}

        if idx % 2 == 0: 
            last = i

        athletes[i["name"]][year][tag]["rank"] = i["rank"]
        
        if "speed" in df:
            athletes[i["name"]][year][tag]["Time"]            = str(i["time"])
            athletes[i["name"]][year][tag]["Speed"]           = str(i["speed"])
        if "Race 1" in df:
            athletes[i["name"]][year][tag]["Race 1"]          = str(i["Race 1"])
            athletes[i["name"]][year][tag]["Speed 1"]         = str(i["Speed 1"])
        if "Race 2" in df:
            athletes[i["name"]][year][tag]["Race 2"]          = str(i["Race 2"])
            athletes[i["name"]][year][tag]["Speed 2"]         = str(i["Speed 2"])
        if "Decider" in df:
            athletes[i["name"]][year][tag]["Decider"]         = str(i["Decider"])
            athletes[i["name"]][year][tag]["Speed Decider"]   = str(i["Speed Decider"])
        
        if idx % 2 == 0: 
            if "speed" in df:
                athletes[i["name"]][year][tag]["Time"]            = str(last["time"])
                athletes[i["name"]][year][tag]["Speed"]           = str(last["speed"])
            if "Race 1" in df:
                athletes[i["name"]][year][tag]["Race 1"]          = str(last["Race 1"])
                athletes[i["name"]][year][tag]["Speed 1"]         = str(last["Speed 1"])
            if "Race 2" in df:
                athletes[i["name"]][year][tag]["Race 2"]          = str(last["Race 2"])
                athletes[i["name"]][year][tag]["Speed 2"]         = str(last["Speed 2"])
            if "Decider" in df:
                athletes[i["name"]][year][tag]["Decider"]         = str(last["Decider"])
                athletes[i["name"]][year][tag]["Speed Decider"]   = str(last["Speed Decider"])
        
        else:
            if "speed" in df:
                athletes[last["name"]][year][tag]["Time"]          = str(i["time"])
                athletes[last["name"]][year][tag]["Speed"]         = str(i["speed"])
            if "Race 1" in df:
                athletes[last["name"]][year][tag]["Race 1"]        = str(i["Race 1"])
                athletes[last["name"]][year][tag]["Speed 1"]       = str(i["Speed 1"])
            if "Race 2" in df:
                athletes[last["name"]][year][tag]["Race 2"]        = str(i["Race 2"])
                athletes[last["name"]][year][tag]["Speed 2"]       = str(i["Speed 2"])
            if "Decider" in df:
                athletes[last["name"]][year][tag]["Decider"]       = str(i["Decider"])
                athletes[last["name"]][year][tag]["Speed Decider"] = str(i["Speed Decider"])
    

df = pd.read_csv("2019/MenSprintQualif.csv", sep=";")


for idx, i in df.iterrows():
    if not i["name"] in athletes:
        athletes[i["name"]] = {}
    athletes[i["name"]]["Country"] = i["country"]
    athletes[i["name"]]["2019"] = {}
    athletes[i["name"]]["2019"]["Qualif"] = {}
        
    athletes[i["name"]]["2019"]["Qualif"]["Rank"]    = str(i["rank"])
    athletes[i["name"]]["2019"]["Qualif"]["100"]     = str(i["100"])
    athletes[i["name"]]["2019"]["Qualif"]["200"]     = str(i["200"])
    athletes[i["name"]]["2019"]["Qualif"]["100-200"] = str(i["100-200"])
    athletes[i["name"]]["2019"]["Qualif"]["Speed"]   = str(i["speed"])

df = pd.read_csv("2019/MenSprint16.csv", sep=";")
add_data(df, "sixteenth")

df = pd.read_csv("2019/MenSprint8.csv", sep=";")
add_data(df, "eighth")


df = pd.read_csv("2019/MenSprint4.csv", sep=";")
add_data(df, "quarter")

df = pd.read_csv("2019/MenSprint2.csv", sep=";")
add_data(df, "semi")

df = pd.read_csv("2019/MenSprint.csv", sep=";")
add_data(df, "final")

df = pd.read_csv("2020/MenSprintQualif.csv", sep=";")


for idx, i in df.iterrows():
    if not i["name"] in athletes:
        athletes[i["name"]] = {}
    athletes[i["name"]]["Country"] = i["country"]
    athletes[i["name"]]["2020"] = {}
    athletes[i["name"]]["2020"]["Qualif"] = {}
        
    athletes[i["name"]]["2020"]["Qualif"]["Rank"]    = str(i["rank"])
    athletes[i["name"]]["2020"]["Qualif"]["100"]     = str(i["100"])
    athletes[i["name"]]["2020"]["Qualif"]["200"]     = str(i["200"])
    athletes[i["name"]]["2020"]["Qualif"]["100-200"] = str(i["100-200"])
    athletes[i["name"]]["2020"]["Qualif"]["Speed"]   = str(i["speed"])

df = pd.read_csv("2020/MenSprint16.csv", sep=",")
add_data(df, "sixteenth", "2020")

df = pd.read_csv("2020/MenSprint8.csv", sep=";")
add_data(df, "eighth", "2020")


df = pd.read_csv("2020/MenSprint4.csv", sep=";")
add_data(df, "quarter", "2020")

df = pd.read_csv("2020/MenSprint2.csv", sep=";")
add_data(df, "semi", "2020")

df = pd.read_csv("2020/MenSprint.csv", sep=";")
add_data(df, "final", "2020")

with open("men_sprint.json", "w") as f:
    f.write(fix_quotes(json.dumps(athletes, indent=True, skipkeys=True)))
    
    