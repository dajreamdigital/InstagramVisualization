import pandas as pd
import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier



class FilterRecommender:
	model = None
	df = None
	def __init__(self):
		#for time of day
		#print 'called init'
		day =  {1:4, 2:4, 3:4, 4:4, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1, 13:2, 14:2, 15:2, 16:2, 17:2, 18:3, 19:3, 20:3, 21:4, 22:4, 23:4, 0:4}
		#for season
		month = {1:4, 2:4, 3:1, 4:1, 5:1, 6:1, 7:2, 8:2, 9:3, 10:3, 11:3, 12:4}
		#image classes
		imageclasses = {'city':0, 'selfie':1, 'fashion':2, 'group': 3, 'food':4, 'animal':5, 'flower':6, 'beach':7, 'nature':8, 'quote':9, 'abstract': 10}


		FilterRecommender.df = pd.read_csv('../data/NewYork_object_detection_final.csv',\
			usecols = ['locationname', 'createdtime', 'image_class1', 'likes', 'comments', 'filter'])

		FilterRecommender.df['timeofday'] = FilterRecommender.df['createdtime'].apply(lambda x: day[int(datetime.datetime.fromtimestamp(int(x)).strftime('%H'))])
		FilterRecommender.df['season'] = FilterRecommender.df['createdtime'].apply(lambda x: month[int(datetime.datetime.fromtimestamp(int(x)).strftime('%m'))])
		FilterRecommender.df['dayofweek'] = FilterRecommender.df['createdtime'].apply(lambda x: datetime.datetime.fromtimestamp(int(x)).weekday())
		FilterRecommender.df['likes'] = FilterRecommender.df['likes'].apply(lambda x: int(x))
		FilterRecommender.df['comments'] = FilterRecommender.df['comments'].apply(lambda x: int(x))

		#Restrict outliers by likes, probably celebrities
		FilterRecommender.df = FilterRecommender.df[FilterRecommender.df.likes <= 100]
		FilterRecommender.df = FilterRecommender.df[FilterRecommender.df.comments <= 100]

		#Clean the data, convert strings to int and stuff
		FilterRecommender.df['image_class1'] = FilterRecommender.df['image_class1'].apply(lambda x: imageclasses[x])

		featurecolumns = ['timeofday', 'image_class1', 'season', 'dayofweek']

		labels = FilterRecommender.df['filter'].values
		features = FilterRecommender.df[list(featurecolumns)].values

		FilterRecommender.model = KNeighborsClassifier()
		FilterRecommender.model.fit(features, labels)


	def getRecommendations(self, inputvector):
		

		#distances, indices = model.kneighbors([[3, 1, 1, 2]], features.shape[0])
		distances, indices = FilterRecommender.model.kneighbors([inputvector], 1000)

		distances = list(distances[0])

		indices = list(indices[0])

		minindices = []
		mindistance = min(distances)

		for i in range(len(distances)):
			if distances[i] == mindistance:
				minindices.append(indices[i])


		#print 'Got', len(minindices), ' min indices with distance',mindistance

		if len(minindices) > 100:
			nearestneighbors = FilterRecommender.df.iloc[minindices]
		else:
			#print 'len indices', len(indices[:100])
			nearestneighbors = FilterRecommender.df.iloc[indices][:100]


		#nearestneighbors = FilterRecommender.df.iloc[indices]

		alpha = 1
		beta = 1

		filterscore = nearestneighbors

		filterscore['likes'] = nearestneighbors['likes'].apply(lambda x: x*alpha)
		filterscore['comments'] = nearestneighbors['comments'].apply(lambda x: x*beta)


		filterscore = nearestneighbors.groupby('filter').agg({'likes': np.sum, 'comments': np.sum})

		filterscore['score'] = filterscore['likes'] + filterscore['comments']

		filterscore = filterscore.sort('likes', ascending=0).iloc[:5]

		return filterscore.index.values

def main():
	filterrecommender = FilterRecommender()
	f = open('../data/FilterRecommendations.txt','w')
	# for imageclass in range(8):
	# 	for timeofday in range(1,5):
	# 		for season in range(1,5):
	# 			for dayofweek in range(7):
	# 				print [timeofday, imageclass, season, dayofweek], filterrecommender.getRecommendations([timeofday, imageclass, season, dayofweek])
	# 				f.write(str([timeofday, imageclass, season, dayofweek]) + str(filterrecommender.getRecommendations([timeofday, imageclass, season, dayofweek])))
	# 				f.write('\n')
	print filterrecommender.getRecommendations([1,3,1,2])

if __name__ == '__main__':
	main()