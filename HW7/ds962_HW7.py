import sys, random,os


def getFeatureData(featureFile, bias = 0):
	
	x = []
	
	dFile = open(featureFile, 'r')
	
	i = 0
	
	for line in dFile:
	
		row = line.split()
		
		rVec = [float(item) for item in row]
		
		if bias > 0:
		
			rVec.insert(0, bias)

		#print('row {} : {}'.format(i,rVec))
 
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


def connectLabels(lsi, n, lsl):
	
	checkList, lstest, lstrain = [i[1] for i in lsl], [], []

	for i in (range(len(lsi))):

		for j in range(len(lsl)):

			if lsl[j][1] == i:

				lsi[i].append(lsl[j][0])
			
		if i not in checkList:

			lstest.append(lsi[i])
			
		else:

			lstrain.append(lsi[i])

	return  lstrain, lstest
	
	
def sorting(featuresList, labelsList):

	n, tempL, tempF = len(featuresList), [], []

	for i in range(n):
		
		x = min(featuresList)
		
		tempL.append(labelsList[featuresList.index(x)])

		tempF.append(x)
		
		labelsList.pop(featuresList.index(x))

		featuresList.pop(featuresList.index(x))

	return tempL, tempF


def gini_index(tempLableList,l_l):

	minimum,split = 1,0

	for j in range(1,len(tempLableList)-1,1):

		L_S,R_S = tempLableList[:j],tempLableList[j:]

		ans = ( ( j / len(tempLableList) ) * ( L_S.count(l_l) / j ) * ( 1 - L_S.count(l_l) / j ) ) + ( ( ( len(tempLableList) - j ) / len(tempLableList) ) * ( R_S.count(l_l) / ( len(tempLableList) - j ) ) * (1 - R_S.count(l_l) / ( len(tempLableList) - j ) ) )

		if ans < minimum:

			minimum = ans

			split = j

	return minimum,split


#opening files
inputList = getFeatureData(sys.argv[1])

labelList = getLabelData(sys.argv[2])

labelList = [[-1 if v == 0 else 1, k] for k, v in labelList.items()]
		
#connecting missing labels with it's features
trainList, testList = connectLabels(inputList, len(inputList[0]), labelList)


def CART(trainList,testList,test,tries):

	finalList = [[0 for _ in trainList] for _ in range(len(trainList[0]))]

	for i in range(len(trainList)):

			for j in range(len(trainList[0])):

				finalList[j][i] = trainList[i][j]

	tempLabelList = [[finalList[-1].copy()] for _ in range(len(finalList)-1)]

	gini, split = [],  []   

	r = finalList.copy()

	for i in range(len(finalList) - 1):

		tempLabelList[i], r[i] =  sorting(finalList[i].copy(), tempLabelList[i][0])

		if tempLabelList[int(i/2)].count(1) >  tempLabelList[int(i/2):].count(1):
			l_l=1
		else:
			l_l=-1
		
		gini.append(gini_index(tempLabelList[i],l_l)[0])

		split.append(gini_index(tempLabelList[i],l_l)[1])

	k = gini.index(min(gini)) 

	s = r[k][split[k]]


	dict = {'column k':k,'split s':s}
	print(dict)
	for n,i in enumerate(testList):
		if i[k]>=s:
			m=-1*l_l
		else:
			m=l_l
		testList[n].append(m)
	fin = tries
	
	for n, i in enumerate(inputList):
		
		for m,j in enumerate(testList):
			
			if i == j:
				if test == 0:

					fin.append([n,j[-1]])
				else:
					fin[m].append(j[-1])
	return fin

tries= []

bagg_n = 100

for i in range(bagg_n):

	inside, bagg_r = [], random.choices([m for m in range(len(trainList))], k = len(trainList))
	
	
	for j in bagg_r:
		
		inside.append(trainList[j])
	tries = CART(inside,testList,i,tries)
	
index = [tries[m].pop(0) for m in range(len(tries))]
label = [sum(tries[m]) for m in range(len(tries))]

for n,i in enumerate(label):
	if i>0:
		label[n] = 1
	else:
		label[n] = 0

	print(label[n],index[n])