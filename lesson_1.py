from pprint import pprint
import requests
import json


main_link = 'https://api.github.com/users/'
user = 'octocat'

response = requests.get(f'{main_link}{user}/repos')

if response.ok:
    data = json.loads(response.text)
# pprint(data)

x = []

for i in response.json():
    x.append(i['name'])

print(f"У пользователя {user} репозитории: {','.join(x)}")

# 2

url = "https://who-covid-19-data.p.rapidapi.com/api/data"
headers = {
    'x-rapidapi-host': "who-covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "fffb18834cmsh6d319706988dcdbp1d69c9jsnfeff4a9a082c"
    }

country = 'Spain'
reportDate = '2020-05-13'
region = "European Region"
querystring = {'name': country,
               "region": region,
               "reportDate": reportDate}
response = requests.get(url, headers=headers, params=querystring)
# print(response.text)

if response.ok:
    data = json.loads(response.text)
# pprint(data)

print(f"В {data[0]['name']} всего {data[0]['cases']} случаев заражения, из них {data[0]['deaths']} смертельных ")


with open('covid.txt', 'w') as f:
    f.write(f"В {data[0]['name']} всего {data[0]['cases']} случаев заражения, из них {data[0]['deaths']} смертельных ")
f.close()
