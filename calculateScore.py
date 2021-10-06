from datetime import datetime
import requests
#import simplejson as json
import json

url = "https://teksas-api.devlabs.id/site/calculatevendorscore/"
res = requests.get(url)

print(res.text)