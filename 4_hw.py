from pymongo import MongoClient
import json


client = MongoClient('localhost', 27017)
db = client['news_data']

mail = db.mail_data
lenta = db.lenta_data
yandex = db.yandex_data

with open('news_mail.json') as f:
    mail_data = json.load(f)

with open('news_lenta.json') as f:
    lenta_data = json.load(f)

with open('news_yandex.json') as f:
    yandex_data = json.load(f)

mail.insert_many(mail_data)
lenta.insert_many(lenta_data)
yandex.insert_many(yandex_data)

