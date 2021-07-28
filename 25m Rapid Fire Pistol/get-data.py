import requests
from parsel import Selector
import os
from typing import List
import json


def getData(pageTex: str) -> dict:
    page = Selector(text=pageTex)
    qualify = page.css('h3+table')[0]
    qualifyData: List[Selector] = qualify.css('tbody > tr')

    data = {}
    currentName: str = ''
    row: Selector
    for row in qualifyData:
        col: Selector
        for n, col in enumerate(row.css("td")):
            if n == 0 or n == 6 or n >= 10:
                continue
            if n == 1:
                currentName = col.css('a::text').get()
                data[currentName] = {}
                data[currentName]['Stage 1'] = {}
                data[currentName]['Stage 2'] = {}
                continue
            if n == 2:
                data[currentName]['nation'] = col.css('a::text').get()
                continue
            data[currentName][f'Stage {n//6+1}'][f"Seconds {2*(n%4)+2+(n%4==0)*4}"] = col.css(
                "::text").get()

    return data


name = 'olymp2012'
if os.path.exists(name + '.html'):
    with open(name + '.html', encoding='utf-8') as f:
        pageTex = f.read()
else:
    pageTex = requests.get(
        'https://en.wikipedia.org/wiki/Shooting_at_the_2012_Summer_Olympics_%E2%80%93_Men%27s_25_metre_rapid_fire_pistol').text
    with open(name + '.html', 'w', encoding='utf-8') as f:
        f.write(pageTex)

olymp2012 = getData(pageTex)
json.dump(olymp2012, open(name + '.json', 'w'), indent=2)


name = 'olymp2016'
if os.path.exists(name + '.html'):
    with open(name + '.html', encoding='utf-8') as f:
        pageTex = f.read()
else:
    pageTex = requests.get(
        'https://en.wikipedia.org/wiki/Shooting_at_the_2016_Summer_Olympics_%E2%80%93_Men%27s_25_metre_rapid_fire_pistol').text
    with open(name + '.html', 'w', encoding='utf-8') as f:
        f.write(pageTex)

olymp2012 = getData(pageTex)
json.dump(olymp2012, open(name + '.json', 'w'), indent=2)
