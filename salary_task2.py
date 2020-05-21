import json
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancy_data']

hh = db.hh_data
sj = db.sj_data

with open('vac_sj.json') as f:
    sj_data = json.load(f)

sj.insert_many(sj_data)

a = int(input('Введите желаемую зарплату '))

vacancies = []

for vacancy in hh.find({'salary_max': {'$gte': a}}).sort('salary_max', -1):
    vacancies.append(vacancy)

for vac in sj.find({'salary_max': {'$gte': a}}).sort('salary_max', -1):
    vacancies.append(vac)

pprint(vacancies)

client.close()


