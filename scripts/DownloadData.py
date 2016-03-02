import requests
from pandas.io.json import json_normalize
import pandas as pd
from tabulate import tabulate

base_url = 'https://api.instagram.com/v1'
ACCESS_TOKEN = 'Please use your own access token'

query = 'atlanta'

url = '{0}/tags/{1}/media/recent?access_token={2}&count=30'.format(base_url, query, ACCESS_TOKEN)
print url

r = requests.get(url)
j = r.json()

results = []

if 'data' in j:
	data = j['data']
	df_instance = json_normalize(data)
	results.append(df_instance)

df = pd.DataFrame().append(results)

print tabulate(df.head(30)[['filter', 'likes.count']], headers='keys', tablefmt='psql')
