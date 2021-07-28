import json

participants = set(map(lambda x: x['name'].lower(
) + ' ' + x['lastName'].lower(), json.load(open('participants.json')).values()))

olymp2012 = set(
    map(lambda x: x.lower(), json.load(open('olymp2012.json')).keys()))

olymp2016 = set(
    map(lambda x: x.lower(), json.load(open('olymp2016.json')).keys()))

inter = participants.intersection(olymp2012)
inter.update(participants.intersection(olymp2016))

print(len(participants), len(inter))
