import requests
from parsel import Selector
import pandas as pd
import json

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
    
for i,item in enumerate(sports_url):
    
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
            
    write_json(sports[i],athletes)
