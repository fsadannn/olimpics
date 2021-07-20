import csv
import pandas
import re
from collections import defaultdict
from pprint import pprint
import json

athletes = defaultdict(lambda: {
    'fencing': [],
    'swiming': [],
    'riding': [],
    'laser-run': [],
    'nation': ''
})

official_list = set()

with open('atheletes.csv', encoding='utf-8') as f:
    for i in csv.DictReader(f):
        name = (i['Family name'].strip() + ' ' +
                i['Given name'].strip()).lower()
        official_list.add(name)
        athletes[name]['nation'] = i['Country'].strip()


def update_athletes(file_name: str):

    xls = pandas.ExcelFile(file_name)
    for sheetNumber in range(len(xls.sheet_names)):
        if xls.sheet_names[sheetNumber][:3] != "Men" or 'Indvidual' in xls.sheet_names[sheetNumber] or 'Team' in xls.sheet_names[sheetNumber] or 'Relay' in xls.sheet_names[sheetNumber]:
            continue

        sheetX = xls.parse(sheetNumber)

        for n, i in enumerate(sheetX['Name']):
            name = i.split('\n')[0].strip().lower()
            if name in official_list:
                if sheetX['Fencing'][n] != 'DNS' and sheetX['Fencing'][n] != 'DNF':
                    fencing_data = sheetX['Fencing'][n].split('\n')[
                        1].split('-')
                    victory = int(re.search('[0-9]+', fencing_data[0]).group())
                    lousse = int(re.search('[0-9]+', fencing_data[1]).group())
                    athletes[name]['fencing'].append(
                        victory / (victory + lousse))

                if sheetX['Swimming'][n] != 'DNS' and sheetX['Swimming'][n] != 'DNF':
                    time_data = sheetX['Swimming'][n].split('\n')[1].split(':')
                    time = int(time_data[0]) * 60 + float(time_data[1])
                    athletes[name]['swiming'].append(time)

                if sheetX['LaserRun'][n] != 'DNS' and sheetX['LaserRun'][n] != 'DNF':
                    time_data = sheetX['LaserRun'][n].split('\n')[1].split(':')
                    time = int(time_data[0]) * 60 + float(time_data[1])
                    gap = 0
                    if not isinstance(sheetX['Time Difference'][n], float):
                        gap = int(re.search(
                            '[0-9]+', sheetX['Time Difference'][n]).group()) / 4
                    athletes[name]['laser-run'].append(time - gap)

                if 'Riding' in sheetX:
                    if sheetX['Riding'][n] != 'DNS' and sheetX['LaserRun'][n] != 'DNF':
                        points_data = sheetX['Riding'][n].split('\n')[0]
                        points = int(re.search('[0-9]+', points_data).group())
                        athletes[name]['riding'].append(points)


update_athletes(
    'Competition_Results_Exports_UIPM_2021_Pentathlon_World_Cup_II.xls')
update_athletes(
    'Competition_Results_Exports_UIPM_2021_Pentathlon_World_Cup_I.xls')
update_athletes(
    'Competition_Results_Exports_2021_Senior_European_Championships.xls')
update_athletes(
    'Competition_Results_Exports_UIPM_2021_Pentathlon_World_Championships.xls')
update_athletes(
    'Competition_Results_Exports_UIPM_2021_Pentathlon_World_Cup_Final.xls')
update_athletes(
    'Competition_Results_Exports_UIPM_2020_Pentathlon_World_Cup.xls')
update_athletes(
    'Competition_Results_Exports_Asia__Oceania_Championships.xls')
update_athletes(
    'Competition_Results_Exports_Pan_American_Games.xls')

# pprint(athletes)

json.dump(athletes, open('data.json', 'w'), indent=2)
