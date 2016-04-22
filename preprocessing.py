import pprint as pp
import json
import pandas as pd
import datetime

with open('template.json', 'r') as f:
      template = json.load(f)

df = pd.read_csv('~/Downloads/Data_NY_LA.csv', usecols = ['filter', 'likes', 'createdtime', 'image_class1'])

#for time of day
#print 'called init'
day =  {1:"night", 2:"night", 3:"night", 4:"night", 5:"morning", 6:"morning", 7:"morning", 8:"morning", 9:"morning", 10:"morning", 11:"morning", 12:"morning", 13:"afternoon", 14:"afternoon", 15:"afternoon", 16:"afternoon", 17:"afternoon", 18:"evening", 19:"evening", 20:"evening", 21:"night", 22:"night", 23:"night", 0:"night"}
#for season
month = {1:"winter", 2:"winter", 3:"spring", 4:"spring", 5:"spring", 6:"spring", 7:"summer", 8:"summer", 9:"fall", 10:"fall", 11:"fall", 12:"winter"}

df['timeofday'] = df['createdtime'].apply(lambda x: day[int(datetime.datetime.fromtimestamp(int(x)).strftime('%H'))])
df['season'] = df['createdtime'].apply(lambda x: month[int(datetime.datetime.fromtimestamp(int(x)).strftime('%m'))])
df['likes'] = df['likes'].apply(lambda x: int(x))

# filter='Lark', likes=12, createdtime=1457510658, image_class1='food', timeofday='night', season='spring'

for row in df.itertuples(index=False):
      template[row[0]]['value'] += 1
      template[row[0]][row[5]] += 1
      template[row[0]][row[4]] += 1
      template[row[0]][row[3]]['count'] += 1
      template[row[0]][row[3]]['likes'] += row[1]

with open('preprocessed.json', 'w') as wf:
      json.dump(template, wf)

