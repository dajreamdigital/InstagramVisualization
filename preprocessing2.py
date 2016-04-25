import pandas as pd
import json
import pdb
import datetime
import numpy as np

df = pd.read_csv('/Users/siddharthshah/Downloads/Washington_object_detection_final.csv', usecols = ['filter', 'comments', 'likes', 'createdtime', 'image_class1'])


day =  {1:"night", 2:"night", 3:"night", 4:"night", 5:"morning", 6:"morning", 7:"morning", 8:"morning", 9:"morning", 10:"morning", 11:"morning", 12:"morning", 13:"afternoon", 14:"afternoon", 15:"afternoon", 16:"afternoon", 17:"afternoon", 18:"evening", 19:"evening", 20:"evening", 21:"night", 22:"night", 23:"night", 0:"night"}
#for season
month = {1:"winter", 2:"winter", 3:"spring", 4:"spring", 5:"spring", 6:"spring", 7:"summer", 8:"summer", 9:"fall", 10:"fall", 11:"fall", 12:"winter"}

df['timeofday'] = df['createdtime'].apply(lambda x: day[int(datetime.datetime.fromtimestamp(int(x)).strftime('%H'))])
df['season'] = df['createdtime'].apply(lambda x: month[int(datetime.datetime.fromtimestamp(int(x)).strftime('%m'))])
df['likes'] = df['likes'].apply(lambda x: int(x))
df['comments'] = df['comments'].apply(lambda x: int(x))

grouped = df.groupby(['image_class1', 'season', 'timeofday', 'filter'])
summed = grouped.aggregate(np.sum)
summed.reset_index(inplace=True)

#image classes
image_classes = ['city', 'selfie', 'fashion', 'group', 'food', 'animal','flower', 'beach','nature', 'quote', 'abstract']

time_of_day = ['morning', 'afternoon', 'evening', 'night']

seasons = ['spring', 'summer', 'fall', 'winter']

with open('template.json', 'r') as f:
	json_data = json.load(f)

filters = json_data.keys()

data = {'name':'Instagram data', 'children': []}

for image_class in image_classes:
	data['children'].append({'name': image_class, 'children': []})
	for season in seasons:
		data['children'][-1]['children'].append({'name': season, 'children': []})
		for time in time_of_day:
			data['children'][-1]['children'][-1]['children'].append({'name': time, 'children': []})
			for img_filter in filters:
				try:
					size = grouped.get_group((image_class, season, time, img_filter))
				except:
					data['children'][-1]['children'][-1]['children'][-1]['children'].append({'name': img_filter, 'size': 0, \
						'likes': 0, \
						'comments': 0})
				else:	
					data['children'][-1]['children'][-1]['children'][-1]['children'].append({'name': img_filter, 'size': grouped.get_group((image_class, season, time, img_filter)).shape[0], \
						'likes': summed[(summed['image_class1'] == image_class) & (summed['season'] == season) & (summed['timeofday'] == time) & (summed['filter'] == img_filter)].likes.item(), \
						'comments': summed[(summed['image_class1'] == image_class) & (summed['season'] == season) & (summed['timeofday'] == time) & (summed['filter'] == img_filter)].comments.item()})

with open('preprocessed2.json', 'w') as pp2:
	json.dump(data, pp2)				