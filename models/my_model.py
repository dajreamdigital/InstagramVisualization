import utils
import numpy as np
import pandas as pd
import os
from time import time
import topic_modelling
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier, VotingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression, Perceptron, LinearRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import dump_svmlight_file
import datetime

month = {1:4, 2:4, 3:1, 4:1, 5:1, 6:1, 7:2, 8:2, 9:3, 10:3, 11:3, 12:4}
day =  {1:4, 2:4, 3:4, 4:4, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1, 13:2, 14:2, 15:2, 16:2, 17:2, 18:3, 19:3, 20:3, 21:4, 22:4, 23:4, 0:4}

def features():
	#TODO: complete this

	events = pd.read_csv('../data/' + 'LosAngeles.csv')
	feature_map = pd.read_csv('../data/' + 'filter_map.csv')
	result = pd.merge(left=events,right=feature_map, on = 'filter')
	result = result.drop('filter',1)
	result = result.rename(columns = { 'idx' : 'filter'})
	result = result[['filter', 'likes', 'comments', 'createdtime']]
	result = result.dropna()
	result['timeofday'] = result['createdtime'].apply(lambda x: day[int(datetime.datetime.fromtimestamp(int(x)).strftime('%H'))])
	result['season'] = result['createdtime'].apply(lambda x: month[int(datetime.datetime.fromtimestamp(int(x)).strftime('%m'))])
	result = result.drop('createdtime',1)

	print(result)


	train = pd.read_csv("../data/LosAngeles.csv", delimiter=",")
	data_samples = train.tags
	topics = topic_modelling.topic_LDA(data_samples)


	agg = pd.concat([result, topics], axis=1, join='inner')
	agg = agg[-agg['filter'].isin([26])]
	agg = agg.sample(frac=0.2, replace=True)


	fil = agg.ix[:,0]
	agg = agg.drop('filter',1)
	dump_svmlight_file(agg, fil, "../data/output.train")

	#
	X_train, Y_train = utils.get_data_from_svmlight("../data/output.train")
	X_test, Y_test = utils.get_data_from_svmlight("../data/output.train")
	#
	return X_train,Y_train,X_test


def my_classifier_predictions(X_train,Y_train,X_test):
	#TODO: complete this
	# clfs = []
	# gbc = GradientBoostingClassifier(n_estimators=620, learning_rate=0.1, max_depth=1,subsample=1.0, random_state=545510477).fit(X_train, Y_train) # 620, 0.1, 1
	# rfc = RandomForestClassifier(n_estimators=100).fit(X_train, Y_train)
	efc = ExtraTreesClassifier(n_estimators=100).fit(X_train, Y_train)
	# dtc = DecisionTreeClassifier(max_depth=25, max_features='log2', random_state=545510477).fit(X_train, Y_train)
	# knn = KNeighborsClassifier().fit(X_train, Y_train)
	# per = Perceptron(n_iter = 35).fit(X_train, Y_train)
	# svc = LinearSVC().fit(X_train, Y_train)
	# lr = LogisticRegression().fit(X_train, Y_train)
	# ada = AdaBoostClassifier(n_estimators=33).fit(X_train.toarray(), Y_train)
	# vote = VotingClassifier(estimators=[('gbc', gbc), ('rfc1', rfc1), ('rfc2', rfc2),('efc1', efc1), ('efc2', efc2), ('dtc',dtc),  ('knn',knn),('lr', lr) , ('ada', ada)], voting='soft' , weights = [10, 2, 5, 1, 1, 3, 4, 2, 2]).fit(X_train, Y_train)
	# params = {'lr__C': [1.0, 100.0], 'gbc__n_estimators': [50, 700],}
	# grid = GridSearchCV(estimator=vote, param_grid=params, cv=5).fit(X_train.toarray(), Y_train)
	# clfs.append(rfc)
	# clfs.append(efc)
	#
	#
	# predictions = []
	#
	# for clf in clfs:
	# 	predictions.append(clf.predict(X_test.toarray()))

	Y_pred = efc.predict(X_test.toarray())

	# Y_pred = np.mean(predictions, axis=0)
	return Y_pred


def main():
	X_train, Y_train, X_test = features()
	# my_features()

	# Y_pred = my_classifier_predictions(X_train,Y_train,X_test)
	# utils.generate_submission("../deliverables/test_features.txt",Y_pred)
	#The above function will generate a csv file of (patient_id,predicted label) and will be saved as "my_predictions.csv" in the deliverables folder.

if __name__ == "__main__":
    main()
