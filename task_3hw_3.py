from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient('localhost', 27017)
db = client['vacancy_data']

sj = db.sj_data

with open('vac_sj_up.json') as f:
    vac_up = json.load(f)
    for i in vac_up:
        sj.update_one({'link': i['link']}, {'$set': i}, upsert=True)
        pprint(i)
