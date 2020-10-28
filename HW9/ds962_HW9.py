import sys, random, os

from sklearn.svm import LinearSVC

from sklearn.model_selection import KFold


def getFeatureData(featureFile, bias = 0):

	x = []

	dFile = open(featureFile, 'r')

	i = 0

	for line in dFile:

		row = line.split()

		rVec = [float(item) for item in row]

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
	
	#print('label : {}'.format(lDict))
		
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

			lstest.append(lsi[i])

			dict[i] = None
			
		else:

			lstrain.append(lsi[i])
	
	return  lstrain, lstest, dict


def initial(zt,ls,w):

	for i in ls:
			
		sum = 0
		
		for n,j in enumerate(w):
			
			sum += w[n]*i[n]
		
		zt.append(sum)

	return zt


def modified(zs, w0):
			
	for i in range(len(zs)):
	
		if w0+zs[i] > 0:
			
			zs[i] = 1
	
		else:
			
			zs[i] = 0
			
	return zs
	
	
def final(Zv, zv):

	for i in range(len(zv)):
	
		Zv[i].append(zv[i])
	
	return Zv

def error_function(answerList, predicted):

	tp, tn, fp, fn = 0, 0, 0, 0
	
	for n,i in enumerate(answerList):

		if answerList[n] == predicted[n]:

			if predicted[n] == 1:
			
				tp += 1

			else:

				tn += 1
		
		elif predicted[n] == 1:

			fp += 1

		else:

			fn += 1

	if fp + tp == 0:

		tp = 1

	if fn + tn == 0:

		tn = 1

	return 0.5 * ((fp / (fp + tp)) + (fn / (fn + tn)))

def error_functiondict(answerList, predicted):

	tp, tn, fp, fn = 0, 0, 0, 0
	
	for n in predicted.keys():

		if answerList[n] == predicted[n]:

			if predicted[n] == 1:
			
				tp += 1

			else:

				tn += 1
		
		elif predicted[n] == 1:

			fp += 1

		else:

			fn += 1

	if fp + tp == 0:

		tp = 1

	if fn + tn == 0:

		tn = 1

	return 0.5 * ((fp / (fp + tp)) + (fn / (fn + tn)))

def random_projection(trainList, testList, dict, k, answerList):

	dict_org = dict.copy()

	Z, Z1, label = [[] for _ in trainList], [[] for _ in testList], [i.pop() for i in (trainList)]

	kf = KFold(n_splits = 5)

	ls_org = []

	C_1 = [0.001, 0.01, 0.1, 1, 10, 100]

	for c in C_1:

		ls_org.append([])

		model_1 =  LinearSVC(max_iter = 10000, C = c)

		for train_index, test_index in kf.split(trainList):
		
			X_train, X_test = [trainList[i1] for i1 in train_index], [trainList[i2] for i2 in test_index]

			y_train, y_test = [label[i1] for i1 in train_index], [label[i2] for i2 in test_index]

			model_1.fit(X_train, y_train)

			y_pred = model_1.predict(X_test)

			ls_org[-1].append(1 - model_1.score(X_test, y_test))		
		
	
	ls_org = [sum(i) / len(i) for i in ls_org]

	model =  LinearSVC(max_iter = 10000, C = C_1[ls_org.index(min(ls_org))])

	C_1 = [0.001, 0.01, 0.1, 1, 10, 100]
	
	model.fit(trainList, label)

	y_pred_org = model.predict(testList)

	for n, i in enumerate(dict_org.keys()):

		dict_org[i] = y_pred_org[n]
	
	for r in range(k):
		
		w, z, z1 = [-2 * random.random() + 1 for _ in range(len(trainList[0]))], [], []
		
		z = initial(z, trainList, w)

		w0 = random.uniform(min(z), max(z))
		
		z = modified(z, w0)
		
		Z = final(Z, z)
		
		z1 = initial(z1, testList, w)

		z1 = modified(z1, w0)
		
		Z1 = final(Z1, z1)
			

	ls=[]

	for c in C_1:

		ls.append([])
		
		model = LinearSVC(C=c,max_iter=10000)
		
		for train_index, test_index in kf.split(Z):
			
			X_train, X_test = [Z[i1] for i1 in train_index], [Z[i2] for i2 in test_index]

			y_train, y_test = [label[i1] for i1 in train_index], [label[i2] for i2 in test_index]

			model.fit(X_train,y_train)
			
			y_pred = model.predict(X_test)
			
			ls[-1].append(error_function(y_test,y_pred))
	 
	ls = [sum(i) / len(i) for i in ls]

	model =  LinearSVC(max_iter = 10000, C = C_1[ls.index(min(ls))])
	
	model.fit(Z, label)
	
	lt = list(model.predict(Z1))

	for n, i in enumerate(sorted(dict.keys())):

		dict[i] = lt[n]
		print(lt[n],i)

	print("For",labelFileName,'split '+str(split[0])+':\nOriginal data: LinearSVC best C =',C_1[ls_org.index(min(ls_org))],'best CV error = '+str(round(min(ls_org) * 100, 1))+'%, test error =',str(round(error_functiondict(answerList,dict_org) * 100,1))+'%')
	
	print('Random hyperplane data:\nFor K = '+str(k)+':\nLinearSVC best C =',C_1[ls.index(min(ls))],'best CV error = '+str(round(min(ls) * 100, 1))+'%, test error = '+str(round(error_functiondict(answerList,dict) * 100, 1))+'%')
	


#opening files
try:

	inputList = getFeatureData(sys.argv[1])

	labelFile = sys.argv[2]

except:

	if len(sys.argv) <= 3:

		print("provide three arguments 1) data file, 2) label file, 3) value of K")

		exit()

labelList = getLabelData(labelFile)

labelFileName = labelFile.split('\\')[-1].split('.')[-3]
split=[int(labelFile.split('\\')[-1].split('.')[-1])]

labelList = [[0 if v == 0 else 1, k] for k, v in labelList.items()]
		
#connecting missing labels with it's features

trainList, testList, dict = connectLabels(inputList, labelList)

try:

	k = int(sys.argv[3])

except:

	if len(sys.argv) <= 3:

		print("provide three arguments 1) data file, 2) label file, 3) value of K")

		exit()

if len(sys.argv) == 5:
	
	answerList = getLabelData(sys.argv[4])

else:

	try:

		answerList = getLabelData('.'.join(labelFile.split('.')[:len(labelFile.split('.'))-2])+'.labels')

	except:

		print("provide .labels file path for test error as fourth argument")

		exit()

random_projection(trainList,testList,dict, k,answerList)
