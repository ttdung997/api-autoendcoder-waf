import csv
import numpy as np
import pandas as pd
import math
from time import gmtime, strftime
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import StratifiedShuffleSplit
from library.regularizeddeepautoencoder import RegularizedDeepAutoencoder
from sklearn.metrics import roc_curve, auc
from keras.preprocessing import sequence
from sklearn import metrics
from sklearn.metrics import average_precision_score, recall_score, precision_score, f1_score,accuracy_score

def report_evaluation_metrics(y_true, y_pred):
    average_precision = average_precision_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, labels=[0, 1], pos_label=1)
    recall = recall_score(y_true, y_pred, labels=[0, 1], pos_label=1)
    f1 = f1_score(y_true, y_pred, labels=[0, 1], pos_label=1)
    acc = accuracy_score(y_true,y_pred)
    print('Average precision-recall score: {0:0.2f}'.format(average_precision))
    print('Precision: {0:0.4f}'.format(precision))
    print('Recall: {0:0.4f}'.format(recall))
    print('F1: {0:0.4f}'.format(f1))
    print('acc: {0:0.4f}'.format(acc))

def get_data(dataset): 
	data= []
	with open(dataset, "r") as f:
		reader = csv.reader(f)
		for row in reader:
			data.append(row) 
		data =  np.array(data)
	return data

def main():

	model_dir_path = './models'
	valid_chars = {'\x00': 1, '\x04': 5, '\x08': 9, '\x0c': 13, '\x10': 17, '\x14': 21, '\x18': 25, '\x1c': 29, ' ': 33, '$': 37, '(': 41, ',': 45, '0': 49, '4': 53, '8': 57, '<': 61, '@': 65, 'D': 69, 'H': 73, 'L': 77, 'P': 81, 'T': 85, 'X': 89, '\\': 93, '`': 97, 'd': 101, 'h': 105, 'l': 109, 'p': 113, 't': 117, 'x': 121, '|': 125, '\x03': 4, '\x07': 8, '\x0b': 12, '\x0f': 16, '\x13': 20, '\x17': 24, '\x1b': 28, '\x1f': 32, '#': 36, "'": 40, '+': 44, '/': 48, '3': 52, '7': 56, ';': 60, '?': 64, 'C': 68, 'G': 72, 'K': 76, 'O': 80, 'S': 84, 'W': 88, '[': 92, '_': 96, 'c': 100, 'g': 104, 'k': 108, 'o': 112, 's': 116, 'w': 120, '{': 124, '\x7f': 128, '\x02': 3, '\x06': 7, '\n': 11, '\x0e': 15, '\x12': 19, '\x16': 23, '\x1a': 27, '\x1e': 31, '"': 35, '&': 39, '*': 43, '.': 47, '2': 51, '6': 55, ':': 59, '>': 63, 'B': 67, 'F': 71, 'J': 75, 'N': 79, 'R': 83, 'V': 87, 'Z': 91, '^': 95, 'b': 99, 'f': 103, 'j': 107, 'n': 111, 'r': 115, 'v': 119, 'z': 123, '~': 127, '\x01': 2, '\x05': 6, '\t': 10, '\r': 14, '\x11': 18, '\x15': 22, '\x19': 26, '\x1d': 30, '!': 34, '%': 38, ')': 42, '-': 46, '1': 50, '5': 54, '9': 58, '=': 62, 'A': 66, 'E': 70, 'I': 74, 'M': 78, 'Q': 82, 'U': 86, 'Y': 90, ']': 94, 'a': 98, 'e': 102, 'i': 106, 'm': 110, 'q': 114, 'u': 118, 'y': 122, '}': 126}

	dataset  = "tokenData/soict/data.csv"

	# Read data from training set and testing set
	data = get_data(dataset)

	anomaly_test_data = []
	anomaly_test_label = []
	nomaly_data =[]
	nomaly_label = []
	for x in data:
		if float(x[-1]) == 1:
			anomaly_test_data.append(x[0])
			anomaly_test_label.append(1)
		else:
			nomaly_data.append(x[0])
			nomaly_label.append(0)

	nomaly_data = np.array(nomaly_data)
	nomaly_label = np.array(nomaly_label)
	anomaly_test_data = np.array(anomaly_test_data)
	anomaly_test_label = np.array(anomaly_test_label)

	maxlen_train = np.max([len(x) for x in nomaly_data])
	maxlen_test = np.max([len(x) for x in anomaly_test_data])
	# Convert characters to int and pad
	maxlen = max(maxlen_train,maxlen_test)
	maxlen = maxlen_train
	split_train_data = StratifiedShuffleSplit(n_splits=1, test_size=0.3,random_state=0)
	for train, test in split_train_data.split(nomaly_data, nomaly_label):
		X_train, nomaly_test_data, y_train, nomaly_test_label = nomaly_data[train], nomaly_data[test], nomaly_label[train], nomaly_label[test]


	nomaly_test_label=nomaly_test_label.astype(int)
	anomaly_test_label=anomaly_test_label.astype(int)
	X_test = np.concatenate((nomaly_test_data,anomaly_test_data), axis=0)
	y_test = np.concatenate((nomaly_test_label,anomaly_test_label), axis=0)
	X_train = [[float(valid_chars[y])/127 for y in x] for x in X_train]

	X_train = sequence.pad_sequences(X_train, maxlen=maxlen,dtype='float')
	X_test = [[float(valid_chars[y])/127 for y in x] for x in X_test]

	X_test = sequence.pad_sequences(X_test, maxlen=maxlen,dtype='float')

	sss =  StratifiedShuffleSplit(n_splits=1, test_size=0.05, random_state=0)
	for train, holdout in sss.split(X_train, y_train):
            X_train, X_holdout, y_train, y_holdout = X_train[train], X_train[holdout], y_train[train], y_train[holdout]
	
	X_train =np.array(X_train)
	X_test =np.array(X_test)
	y_test =np.array(y_test)
	X_train=X_train.astype(float)
	X_test=X_test.astype(float)
	y_test=y_test.astype(int)
	encoder_dim = 200
	encoder_dim_2 = 250
	# VAE =Autoencoder()
	# VAE.fit(X_train,validate_data = X_holdout,validate_label=y_holdout,
	# 	model_dir_path=model_dir_path,epochs = 10,input_dim=maxlen,encoding_dim=encoder_dim)

	# DAE = DeepAutoencoder()
	# DAE.fit(X_train,validate_data = X_holdout,validate_label=y_holdout,
	# 	model_dir_path=model_dir_path,epochs = 10,input_dim=maxlen,encoding_dim=encoder_dim_2)

	# RAE = RegularizedAutoencoder()
	# RAE.fit(X_train,validate_data = X_holdout,validate_label=y_holdout,
	# 	model_dir_path=model_dir_path,epochs = 10,input_dim=maxlen,encoding_dim=encoder_dim)

	RDAE = RegularizedDeepAutoencoder()
	RDAE.fit(X_train,validate_data = X_holdout,validate_label=y_holdout,
		model_dir_path=model_dir_path,epochs = 10,input_dim=maxlen,encoding_dim=encoder_dim_2) 


	print("Finish Training Pharse!")

	std = 1.5
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	
	while std < 5:
		# std = std + 0.5
		print("number of STD: ",std)
	
		print("-----------------Regularized Deep Autoencoder------------------------")
		RDAE = RegularizedDeepAutoencoder()
		RDAE.load_model(model_dir_path)
		print("std :",std)
		y_predict = []
		RDAE.setThresholdStd(X_holdout,std,model_dir_path)
		reconstruction_error = []
		anomaly_information = RDAE.anomaly(X_test)
		for idx, (is_anomaly, dist) in enumerate(anomaly_information):
			# print('# ' + str(idx) + ' is ' + ('abnormal' if is_anomaly else 'normal') + ' (dist: ' + str(dist) + ')')
			reconstruction_error.append(dist)
			if is_anomaly:
				y_predict.append(1)
			else:
				y_predict.append(0)

		report_evaluation_metrics(y_test,y_predict)
		print("Final report!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		report = metrics.classification_report(y_test,y_predict,digits=4)
		print ('\n clasification report:\n', report)
		break


if __name__ == '__main__':
	main()
