import json
import pandas as pd

df = pd.read_csv('Athletes/Road_cycling.csv')

with open('men_road_race.json') as f:
    athletes = json.loads(' '.join(f.readlines()))

excluded = {}
for i in athletes:
    if not i.lower() in df.name:
        excluded[i] = athletes[i]
        athletes.pop(i)

with open('excluded_road.json', 'w') as f:
    f.write(json.dumps(excluded, indent=True, skipkeys=True))

with open('men_road_race.json', 'w') as f:
    f.write(json.dumps(athletes, indent=True, skipkeys=True))
