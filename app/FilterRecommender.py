import pandas as pd
import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier



class FilterRecommender:
	model = None
	df = None
	#for time of day
	#print 'called init'
	day =  {1:4, 2:4, 3:4, 4:4, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1, 13:2, 14:2, 15:2, 16:2, 17:2, 18:3, 19:3, 20:3, 21:4, 22:4, 23:4, 0:4}
	#for season
	month = {1:4, 2:4, 3:1, 4:1, 5:1, 6:1, 7:2, 8:2, 9:3, 10:3, 11:3, 12:4}
	#image classes
	imageclasses = {'city':0, 'selfie':1, 'fashion':2, 'group': 3, 'food':4, 'animal':5, 'flower':6, 'beach':7, 'nature':8, 'quote':9, 'abstract': 10}
	
	def __init__(self):
		FilterRecommender.df = pd.read_csv('../data/Data_NY_LA.csv',\
			usecols = ['locationname', 'createdtime', 'image_class1', 'likes', 'comments', 'filter'])

		FilterRecommender.df['timeofday'] = FilterRecommender.df['createdtime'].apply(lambda x: FilterRecommender.day[int(datetime.datetime.fromtimestamp(int(x)).strftime('%H'))])
		FilterRecommender.df['season'] = FilterRecommender.df['createdtime'].apply(lambda x: FilterRecommender.month[int(datetime.datetime.fromtimestamp(int(x)).strftime('%m'))])
		FilterRecommender.df['dayofweek'] = FilterRecommender.df['createdtime'].apply(lambda x: datetime.datetime.fromtimestamp(int(x)).weekday())
		FilterRecommender.df['likes'] = FilterRecommender.df['likes'].apply(lambda x: int(x))
		FilterRecommender.df['comments'] = FilterRecommender.df['comments'].apply(lambda x: int(x))

		#Restrict outliers by likes, probably celebrities
		FilterRecommender.df = FilterRecommender.df[FilterRecommender.df.likes <= 1000]
		FilterRecommender.df = FilterRecommender.df[FilterRecommender.df.comments <= 1000]

		#Clean the data, convert strings to int and stuff
		FilterRecommender.df['image_class1'] = FilterRecommender.df['image_class1'].apply(lambda x: FilterRecommender.imageclasses[x])

		featurecolumns = ['timeofday', 'image_class1', 'season', 'dayofweek']

		labels = FilterRecommender.df['filter'].values
		features = FilterRecommender.df[list(featurecolumns)].values

		FilterRecommender.model = KNeighborsClassifier()
		FilterRecommender.model.fit(features, labels)


	def getRecommendations(self, inputv):
		

		#distances, indices = model.kneighbors([[3, 1, 1, 2]], features.shape[0])
		#Get required features from inputvector[imageclass, createdtime]
		createdtime = inputv[1]
		imageclass = FilterRecommender.imageclasses[inputv[0]]
		inputvector = [FilterRecommender.day[int(datetime.datetime.fromtimestamp(int(createdtime)).strftime('%H'))],\
			imageclass,\
			FilterRecommender.month[int(datetime.datetime.fromtimestamp(int(createdtime)).strftime('%m'))],\
			datetime.datetime.fromtimestamp(int(createdtime)).weekday()]
		distances, indices = FilterRecommender.model.kneighbors([inputvector], 1000)

		distances = list(distances[0])

		indices = list(indices[0])

		minindices = []
		mindistance = min(distances)

		for i in range(len(distances)):
			if distances[i] == mindistance:
				minindices.append(indices[i])

		if len(minindices) > 100:
			nearestneighbors = FilterRecommender.df.iloc[minindices]
		else:
			nearestneighbors = FilterRecommender.df.iloc[indices][:100]

		alpha = 1
		beta = 1

		filterscore = nearestneighbors

		filterscore['likes'] = nearestneighbors['likes'].apply(lambda x: x*alpha)
		filterscore['comments'] = nearestneighbors['comments'].apply(lambda x: x*beta)

		filterscore = nearestneighbors.groupby('filter').agg({'likes': np.sum, 'comments': np.sum})
		
		filterscore['score'] = filterscore['likes'] + filterscore['comments']

		#Penalize Clarendon
		for idx, row in filterscore.iterrows():
			row['score'] = row['score'] * 0.5 if idx == 'Clarendon' else row['score']

		filterscore = filterscore.reset_index()
		filterscore = filterscore.sort('score', ascending=False)

		return filterscore['filter'].values[:5]

def main():
	filterrecommender = FilterRecommender()
	print filterrecommender.getRecommendations(['selfie',1457510658])

if __name__ == '__main__':
	main()