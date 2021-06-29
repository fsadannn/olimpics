import requests
from parsel import Selector
import pandas as pd
import json
import math

base = 'https://en.wikipedia.org/wiki/'
sports_url = [
    "_UCI_Track_Cycling_World_Championships_–_Women%27s_sprint",
    "_UCI_Track_Cycling_World_Championships_–_Men%27s_sprint"
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_1_km_time_trial",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_1_km_time_trial",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_individual_pursuit",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_individual_pursuit",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_team_pursuit",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_team_pursuit",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_team_sprint",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_team_sprint",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_keiring",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_keiring",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_scratch",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_scratch",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_points_race",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_points_race",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_individual_madison",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_individual_madison",
    
    # "_UCI_Track_Cycling_World_Championships_–_Women%27s_individual_omnium",
    # "_UCI_Track_Cycling_World_Championships_–_Men%27s_individual_omnium",
    
]

sports = [
    'women_sprint',
    'men_sprint'
    # 'women_time_trial', 
    # 'men_time_trial', 
    # 'women_individual_pursuit', 
    # 'men_individual_pursuit', 
    # 'women_team_pursuit',
    # 'men_team_pursuit', 
    # 'women_team_sprint',
    # 'men_team_sprint', 
    # 'women_keiring',
    # 'men_keiring',
    # 'women_scratch',
    # 'men_scratch',
    # 'women_pints_race',
    # 'men_pints_race',
    # 'women_individual_madison'
    # 'men_individual_madison'
    # 'women_individual_omnium'
    # 'men_individual_omnium'
    ]
    
def write_json(sport,data):
    filename = sport+'.json'

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

    
    
def format_data(df, year, round):
        di = df.to_dict(orient='records')

        for entry in di:
            name = entry['Name']
            entry.pop('Name')
            if 'Unnamed' in entry: 
                entry.pop('Unnamed')
            if not name in athletes:
                athletes[name] = {
                    str(year) : {
                        str(round): entry
                    } 
                }
            if not year in athletes[name]:
                athletes[name][year] = {
                    str(round): entry
                }
            else:    
                athletes[name][year][round] = entry
    
for ind,item in enumerate(sports_url):
    
    athletes = {}
    
    for j in range(2017,2021):
            
        url = base+str(j)+item
        text = requests.get(url).text
        selector = Selector(text=text)
        
        
        selectors = ['//*[@id="mw-content-text"]/div[1]/table[2]',
                     '//*[@id="mw-content-text"]/div[1]/table[3]',
                     '//*[@id="mw-content-text"]/div[1]/table[4]',
                     '//*[@id="mw-content-text"]/div[1]/table[5]',
                     '//*[@id="mw-content-text"]/div[1]/table[6]',
                     '//*[@id="mw-content-text"]/div[1]/table[7]'
                    ]
        
        if j > 2018:
            selectors = ['//*[@id="mw-content-text"]/div[1]/table[3]',
                         '//*[@id="mw-content-text"]/div[1]/table[4]',
                         '//*[@id="mw-content-text"]/div[1]/table[5]',
                         '//*[@id="mw-content-text"]/div[1]/table[6]',
                         '//*[@id="mw-content-text"]/div[1]/table[7]',
                         '//*[@id="mw-content-text"]/div[1]/table[8]'
                        ]
        rounds = [
            'qualifying',
            'sixteenth',
            'eighth',
            'quarter',
            'semi',
            'final'
        ]

            
        for idx in range(0,len(selectors)):
            df = pd.read_html(selector.xpath(selectors[idx]).getall()[0])[0]
            format_data(df,j,rounds[idx])

    fact = 1
#TODO Buscar quien es el contrincante de cada atleta y en cada heat ver el resultado en la carrera anterior para acualizar la formula a fact*abs(lugar1-lugar2)/2
    #print(athletes)
    exclude = ['Gold medal final', 'Bronze medal race', 'Gold medal race', 'Bronze medal final']
    for i in athletes.keys():
        if i in exclude:
            continue
        for j in athletes[i].keys():
                if 'sixteenth' in athletes[i][j].keys():
                    try:
                        if str(athletes[i][j]['sixteenth']['Gap']) != 'nan':
                            athletes[i][j]['sixteenth']['Time'] = (float(athletes[i][j]['qualifying']['Time']) + float(athletes[i][j]['sixteenth']['Gap']))
                        else:
                            athletes[i][j]['sixteenth']['Time'] = float(athletes[i][j]['qualifying']['Time'])
                    except:
                        athletes[i][j]['sixteenth']['Time'] = float(athletes[i][j]['qualifying']['Time'])

                    athletes[i][j]['sixteenth']['Time'] = float(athletes[i][j]['sixteenth']['Time']) + (fact * (float(athletes[i][j]['qualifying']['Rank']))/2)
                
                if 'eighth' in athletes[i][j].keys():
                    if str(athletes[i][j]['eighth']['Gap']) == 'nan' or str(athletes[i][j]['eighth']['Gap']) == 'X':
                        if 'sixteenth' in athletes[i][j].keys():
                            athletes[i][j]['eighth']['Time'] = athletes[i][j]['sixteenth']['Time']
                        else:
                            athletes[i][j]['eighth']['Time'] = athletes[i][j]['qualifying']['Time']
                    else: 
                        if 'sixteenth' in athletes[i][j].keys():
                            try:
                                athletes[i][j]['eighth']['Time'] = (float(athletes[i][j]['sixteenth']['Time']) + float(athletes[i][j]['eighth']['Gap']))
                            except:
                                athletes[i][j]['eighth']['Time'] = math.inf
                        else:
                            athletes[i][j]['eighth']['Time'] = (float(athletes[i][j]['qualifying']['Time']) + float(athletes[i][j]['eighth']['Gap']))

                    if 'sixteenth' in athletes[i][j].keys():
                        athletes[i][j]['eighth']['Time'] = float(athletes[i][j]['eighth']['Time']) + (fact * (float(athletes[i][j]['sixteenth']['Rank']))/2)
                    else:
                        athletes[i][j]['eighth']['Time'] = float(athletes[i][j]['eighth']['Time']) + (fact * (float(athletes[i][j]['qualifying']['Rank']))/2)

                if 'quarter' in athletes[i][j].keys():
                    if athletes[i][j]['quarter']['Race 1'] == 'X': 
                        athletes[i][j]['quarter']['Time'] = athletes[i][j]['eighth']['Time']
                    else: 
                        athletes[i][j]['quarter']['Time'] = (athletes[i][j]['eighth']['Time'] + float(athletes[i][j]['quarter']['Race 1']))
                    
                    if athletes[i][j]['quarter']['Race 2'] == 'X': 
                        athletes[i][j]['quarter']['Time'] += athletes[i][j]['eighth']['Time']
                    else: 
                        athletes[i][j]['quarter']['Time'] += (athletes[i][j]['eighth']['Time'] + float(athletes[i][j]['quarter']['Race 2']))
                    
                    if not str(athletes[i][j]['quarter']['Decider (i.r.)']) == 'nan':
                        if athletes[i][j]['quarter']['Decider (i.r.)'] == 'REL[A]':
                            athletes[i][j]['quarter']['Time'] = math.inf
                        elif athletes[i][j]['quarter']['Decider (i.r.)'] != 'X':
                            athletes[i][j]['quarter']['Time'] += (athletes[i][j]['eighth']['Time'] + float(athletes[i][j]['quarter']['Decider (i.r.)']))
                        else:
                            athletes[i][j]['quarter']['Time'] += athletes[i][j]['eighth']['Time']
                        athletes[i][j]['quarter']['Time'] /= 3
                    else: 
                        athletes[i][j]['quarter']['Time'] /= 2

                    athletes[i][j]['quarter']['Time'] = athletes[i][j]['quarter']['Time'] + (fact * (athletes[i][j]['eighth']['Rank'])/2)

                
                if 'semi' in athletes[i][j].keys():               
                    if athletes[i][j]['semi']['Race 1'] == 'X': 
                        athletes[i][j]['semi']['Time'] = athletes[i][j]['quarter']['Time']
                    else: 
                        athletes[i][j]['semi']['Time'] = (athletes[i][j]['quarter']['Time'] + float(athletes[i][j]['semi']['Race 1']))
                    
                    if athletes[i][j]['semi']['Race 2'] == 'X': 
                        athletes[i][j]['semi']['Time'] += athletes[i][j]['quarter']['Time']
                    else: 
                        athletes[i][j]['semi']['Time'] += (athletes[i][j]['quarter']['Time'] + float(athletes[i][j]['semi']['Race 2']))
                    
                    if not str(athletes[i][j]['semi']['Decider (i.r.)']) == 'nan':
                        if athletes[i][j]['semi']['Decider (i.r.)'] != 'X': 
                            athletes[i][j]['semi']['Time'] += (athletes[i][j]['quarter']['Time'] + float(athletes[i][j]['semi']['Decider (i.r.)']))
                        else:
                            athletes[i][j]['semi']['Time'] += athletes[i][j]['quarter']['Time']
                        athletes[i][j]['semi']['Time'] /= 3
                    else: 
                        athletes[i][j]['semi']['Time'] /= 2
                
                    athletes[i][j]['semi']['Time'] = athletes[i][j]['semi']['Time'] + (fact * (athletes[i][j]['quarter']['Rank'])/2)

                if 'final' in athletes[i][j].keys():
                    if athletes[i][j]['final']['Race 1'] == 'REL':
                        athletes[i][j]['final']['Time'] = math.inf

                    elif athletes[i][j]['final']['Race 1'] == 'X':
                        athletes[i][j]['final']['Time'] = athletes[i][j]['semi']['Time']
                    else: 
                        athletes[i][j]['final']['Time'] = (athletes[i][j]['semi']['Time'] + float(athletes[i][j]['final']['Race 1']))
                    
                    if athletes[i][j]['final']['Race 2'] == 'X': 
                        athletes[i][j]['final']['Time'] += athletes[i][j]['semi']['Time']
                    else: 
                        athletes[i][j]['final']['Time'] += (athletes[i][j]['semi']['Time'] + float(athletes[i][j]['final']['Race 2']))
                    
                    if not str(athletes[i][j]['final']['Decider (i.r.)']) == 'nan':
                        if athletes[i][j]['final']['Decider (i.r.)'] != 'X': 
                            athletes[i][j]['final']['Time'] += (athletes[i][j]['semi']['Time'] + float(athletes[i][j]['final']['Decider (i.r.)']))
                        else:
                            athletes[i][j]['final']['Time'] += athletes[i][j]['semi']['Time']
                        athletes[i][j]['final']['Time'] /= 3
                    else: 
                        athletes[i][j]['final']['Time'] /= 2

                    athletes[i][j]['final']['Time'] = athletes[i][j]['final']['Time'] + (fact * (athletes[i][j]['semi']['Rank'])/2)

    write_json(sports[ind],athletes)
