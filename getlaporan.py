from datetime import datetime
import requests
#import simplejson as json
import json

today = datetime.today()
datem = datetime(today.year, today.month, 1)

month = today.month - 1
year = today.year

if month == 0:
    month = 12
    year = year - 1

url = "https://teksas-api.devlabs.id/util/getLaporan/"
res = requests.get(url)

print(res.text)