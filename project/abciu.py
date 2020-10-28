import sys
from sklearn.model_selection import train_test_split
from array import array
from sklearn.linear_model import LogisticRegression
import math
from datetime import datetime
def varianc(XPs, XPs_mean):
	
	sum = 0
	
	for i in (XPs):
		
		sum += ((1 / (len(XPs) - 1))) * (i - XPs_mean) ** 2
	
	sum = sum ** (1 / 2)
	
	return sum
	

def chi_squared(pos, negative):
    
	clas_p = []
    
	clas_n = []
        
	exp_clas_p = []
    
	exp_clas_n = []

	pos_prop = len(pos) / (len(pos + negative))
    
	neg_prop = len(negative) / len((pos + negative))
    
    
	for i in sorted(set(pos+neg)):
        
		clas_p.append(pos.count(i))              
        
		clas_n.append(negative.count(i))
        
		exp_clas_p.append(int((pos+negative).count(i) * pos_prop))
        
		exp_clas_n.append(int((pos+negative).count(i) * neg_prop))
        
	chi_sq = 0
    
	for o,e in zip((clas_p+clas_n),(exp_clas_p+exp_clas_n)):
        
		if e == 0:
            
			chi_sq = 0
        
		else:

			chi_sq += ((o - e) ** 2) / e

	return chi_sq


def getFeatureData(featureFile, bias = 0):

	x = []

	dFile = open(featureFile, 'r')

	i = 0

	for line in dFile:

		row = line.split()

		rVec = array('f',[float(item) for item in row])

		if bias > 0:

			rVec.insert(0, bias)

		x.append(rVec)        

		i += 1

	dFile.close()

	return x


def getLabelData(labelFile, hyperPlaneClass = False):

	lFile = open(labelFile, 'r')
	
	lDict = {}
	
	for line in lFile:
	
		row = line.split()
			
		if hyperPlaneClass and int(row[0]) <= 0:
		
			lDict[int(row[1])] = -1
		
		else:
			
			lDict[int(row[1])] = int(row[0])
	
	lFile.close()
	
	return lDict


def connectLabels(lsi, lsl):
	
	checkList, lstest, lstrain = [i[1] for i in lsl], [], []

	dict = {}
	
	for i in (range(len(lsi))):

		for j in range(len(lsl)):

			if lsl[j][1] == i:

				lsi[i].append(lsl[j][0])
			
		if i not in checkList:

			lstest.append(array('f',lsi[i]))

			dict[i] = None
			
		else:

			lstrain.append(array('f',lsi[i]))
	
	return  lstrain, lstest, dict


def first_n_features(n,fs_cols):
    
	fs_col = array('f',list(fs_cols).copy())
	
	fs_col.pop(fs_cols.index(max(fs_col)))
	
	min_feature,vla=[],[]
    
	for _ in range(n):
		
		maxed = fs_cols.index(max(fs_col))
		
		if len(min_feature)>0 and maxed in min_feature:
			
			maxed += fs_cols[maxed:].index(max(fs_col)) + 1
		
		min_feature.append(maxed)

		fs_col.pop(fs_col.index(max(fs_col)))
		
	return min_feature

t1 =datetime.now()
if len(sys.argv) == 4:
	
	inputList = getFeatureData(sys.argv[1])

	testList = getFeatureData(sys.argv[3])

	labelList = getLabelData(sys.argv[2])
	
else:
	
	try:
		
		inputList = getFeatureData('traindata')

		testList = getFeatureData('testdata')

		labelList = getLabelData('trainingLabels.txt')

	except:
		
		print("provide path to traindata, trainLabels.txt and testdata")
		
		exit()

try:
	labelList = [[v, k] for k, v in labelList.items()]

	#connecting missing labels with it's features
	trainList, _, dict = connectLabels(inputList, labelList)
except:

		print("provide path to traindata, trainLabels.txt and testdata")
		
		exit()
t2 =datetime.now()
print("fileREad",t2-t1)
ch_colm = []
lb = [i[-1] for i in trainList]

for j in range(len(trainList[1])):
    
	positive=array('f',[])
    
	neg=array('f',[])

	for i in trainList[:len(trainList)]:
        
		if(i[-1] == 1):
            
			positive.append(i[j])
        
		else:
            
			neg.append(i[j])
	
	ch_colm.append(chi_squared(positive, neg))

model = LogisticRegression()

y_pred = [[] for _ in range(len(testList))]

for i in range(15,30):	

	ans = first_n_features(i, array('f',list(ch_colm).copy()))
		
	X = [[] for _ in range(len(trainList))]

	y = [int(i[-1]) for i in trainList]

	x_test = [[] for _ in range(len(testList))]

	for n, i in enumerate(trainList):
			
		for j in ans:
		
			X[n].append(i[j])
		
	for n, i in enumerate(testList):
			
		for j in ans:
			
			x_test[n].append(i[j])

		
	model.fit(X, y)
	
	ls = list(model.predict(x_test))
	
	for i in range(len(y_pred)):
		
		y_pred[i].append(-1 if ls[i] == 0 else 1)

for n,i in enumerate(y_pred):
	symb = 0 if sum(i)//abs(sum(i)) <0 else 1
	prib = int((((len(i))+abs(sum(i)))/len(i))*50)
	print(symb,prib,n)