import my_model
from sklearn.cross_validation import KFold, ShuffleSplit
from numpy import mean
import models

import utils

#input: training data and corresponding labels
#output: accuracy, auc
def get_acc_auc_kfold(X,Y,k=10):
	#TODO:First get the train indices and test indices for each iteration
	#Then train the classifier accordingly
	#Report the mean accuracy and mean auc of all the folds
	accuracy = 0
	auc_curve = 0
	kf_total = KFold(Y.size, n_folds=k)
	for train_indices, test_indices in kf_total:
		lr = my_model.my_classifier_predictions(X[train_indices], Y[train_indices], X[test_indices])
		acc , p , r , f = models.classification_metrics(lr, Y[test_indices])
		accuracy += acc
	return accuracy/k


#input: training data and corresponding labels
#output: accuracy, auc
def get_acc_auc_randomisedCV(X,Y,iterNo=5,test_percent=0.2):
	#TODO: First get the train indices and test indices for each iteration
	#Then train the classifier accordingly
	#Report the mean accuracy and mean auc of all the iterations
	accuracy = 0
	auc_curve = 0
	rs = ShuffleSplit(Y.size, n_iter=iterNo, test_size=test_percent)
	for train_indices, test_indices in rs:
		lr = my_model.my_classifier_predictions(X[train_indices], Y[train_indices], X[test_indices])
		acc, p , r , f = models.classification_metrics(lr, Y[test_indices])
		accuracy += acc
	return accuracy/iterNo


def main():
	X,Y = utils.get_data_from_svmlight("../data/output.train")
	print "Classifier: Logistic Regression__________"
	acc_k = get_acc_auc_kfold(X,Y)
	print "Average Accuracy in KFold CV: "+str(acc_k)
	acc_r = get_acc_auc_randomisedCV(X,Y)
	print "Average Accuracy in Randomised CV: "+str(acc_r)

if __name__ == "__main__":
	main()
