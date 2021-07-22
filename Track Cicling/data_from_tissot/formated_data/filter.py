import json
import pandas as pd


def order_name(string):
    words = string.split()
    for i,word in enumerate(words):
        if word.upper() == word:
            words = words[i+1:]+words[:i+1]
            return ' '.join(words)
def filter(atlhetes, df):
    ath = {}
    for i in athletes:
        order_name(i)
        if order_name(i) in df.name.tolist():
            ath[i] = athletes[i]
    return ath
# with open('excluded_road.json', 'w') as f:
#     f.write(json.dumps(excluded, indent=True, skipkeys=True))
df = pd.read_csv('Athletes/Road_cycling.csv')

with open('men_road_race.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('men_road_race.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_road_race.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_road_race.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

df = pd.read_csv('Athletes/MTB_athletes.csv')

with open('men_mountain.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('men_mountain.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_mountain.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_mountain.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

df = pd.read_csv('Athletes/track_cycling.csv')

with open('women_individual_pursuit.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_individual_pursuit.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_team_pursuit.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_team_pursuit.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_keiring.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_keiring.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))


with open('women_madison.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_madison.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_omnium.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_omnium.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_scratch.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_scratch.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))

with open('women_time_trial.json') as f:
    athletes = json.loads(' '.join(f.readlines()))
with open('women_time_trial.json', 'w') as f:
    f.write(json.dumps(filter(athletes,df), indent=True, skipkeys=True))
