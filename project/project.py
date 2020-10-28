
import sys
import csv
import math
import subprocess
import random as rnd
from operator import itemgetter
import gzip


##############-----Load the data and class labels-----####################
# read file and return a 2d matrix
def read_file(filename):
	with open(filename, 'r') as f:
		reader = f.read()
		data = []
		for rows in reader:
			temp = []
			for col in rows:
				if (col == 1 or col == 0 or col == 2):
					temp.append(int(col))
			data.append(temp)
		return data

# creates input file based on liblinear input format
def liblinear_data_format(X, y, output_file):
	opt = open(output_file, 'w')
	for i in range(0, len(X)):
		opt.write('{} '.format(y[i]))
		for j in range(0, len(X[0])):
			if X[i][j] != 0:
				opt.write('{}:{} '.format(j+1, X[i][j]))
		opt.write('\n')
	opt.close()

# read the label file and return a vector
def extract_train_labels(filename):
	f = open(filename, 'r')
	Original = {}
	l = f.readline()
	while( l != ''):
		a = l.split()
		Original[int(a[1])] = int(a[0])
		l = f.readline()
	f.close()
	V = [Original[i][0] for i in range(0, len(Y))]
	return V

# wtire the prediction of the learning algorithm into a file using class project specification
def write_output_file(filename):
	y = read_file(filename)
	opt = open('predicted_testclass.txt', 'w')
	for i in range(0, len(y)):
		opt.write('{} {}'.format(y[i][0], i))
		opt.write('\n')
	opt.close()

################################-----Learning algorithm-----#########################################
##########################-----Chi-square feature selection-----#######################################
# X: input dataset
# y: input data labels
# top: how many features to used for taining and testing
def chi_sqr(X, y, top):
	rows = len(X)
	cols = len(X[0])
	T = []
	for j in range(0, cols):
	    ct = [[1,1],[1,1],[1,1]]    # contingency table
	    for i in range(0, rows):
	        if y[i] == 0:
	            if X[i][j] == 0:
	                ct[0][0] += 1
	            elif X[i][j] == 1:
	                ct[1][0] += 1
	            elif X[i][j] == 2:
	                ct[2][0] += 1
	        elif y[i] == 1:
	            if X[i][j] == 0:
	                ct[0][1] += 1
	            elif X[i][j] == 1:
	                ct[1][1] += 1
	            elif X[i][j] == 2:
	                ct[2][1] += 1
	    col_totals = [ sum(x) for x in ct]
	    row_totals = [ sum(x) for x in zip(*ct) ]
	    total = sum(col_totals)
	    exp_value = [[(row*col)/total for row in row_totals] for col in col_totals]
	    sqr_value = [[((ct[i][j] - exp_value[i][j])**2)/exp_value[i][j] for j in range(0,len(exp_value[0]))] for i in range(0,len(exp_value))]
	    x_2 = sum([sum(x) for x in zip(*sqr_value)])
	    T.append(x_2)
	indices = sorted(range(len(T)), key=T.__getitem__, reverse=True)
	idx = indices[:top]
	return idx

##############################-----Extract top 15 features-----##########################################
# X: dataset
# cols: columns number with highest chi-square score
# returns: new dataset, size 8000x15
def feature_extraction(X, cols):
	V = []
	columns = list(zip(*X))
	for j in cols:
		V.append(columns[j])
	V = list(zip(*V))
	return V

def feature_ranking_selection(file_train_data, file_train_labels, file_test_data, trainfile, testfile):
	X_train = read_file(file_train_data)					#read training data file
	y_train = extract_train_labels(file_train_labels)		#read training data labels

	idx = chi_sqr(X_train, y_train, 15)						#calculate chi-square and ranked them by decending order and get index of top 15 features

	X_train = feature_extraction(X_train, idx)				# create new training dataset using top 15 features, its size is 8000x15
	liblinear_data_format(X_train, y_train, trainfile)		# create a file with training dataset in liblinear file format

	X_test = read_file(file_test_data)						#read training data file

	X_test = feature_extraction(X_test, idx)				# create new testing dataset using top 15 features, its size is 8000x15
	liblinear_data_format(X_test, y_train, testfile)		# create a file with testing dataset in liblinear file format

	print('Number of feature used: 15')
	print('Columns used in prediction: {}'.format(idx))

if __name__ == '__main__':
	file_train = sys.argv[1]								# training dataset
	file_tlabels = sys.argv[2]								# training labels
	file_test = sys.argv[3]									# testing dataset

	feature_ranking_selection(file_train, file_tlabels, file_test, 'train.data', 'test.data')

	#write_output_file('./predictions')		# read the output produced by linlinear and create a output file based on project specification
