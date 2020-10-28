import sys


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

	for _ in range(n):
		
		x = min(featuresList)
		
		tempL.append(labelsList[featuresList.index(x)])

		tempF.append(x)
		
		labelsList.pop(featuresList.index(x))

		featuresList.pop(featuresList.index(x))

	return tempL, tempF


def gini_index(tempLableList):

	minimum,split = 1,0

	for j in range(1,len(tempLableList)-1,1):

		L_S,R_S = tempLableList[:j],tempLableList[j:]

		ans = ( ( j / len(tempLableList) ) * ( L_S.count(-1) / j ) * ( 1 - L_S.count(-1) / j ) ) + ( ( ( len(tempLableList) - j ) / len(tempLableList) ) * ( R_S.count(-1) / ( len(tempLableList) - j ) ) * (1 - R_S.count(-1) / ( len(tempLableList) - j ) ) )

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

finalList = [[0 for _ in trainList] for _ in range(len(trainList[0]))]

for i in range(len(trainList)):

		for j in range(len(trainList[0])):

			finalList[j][i] = trainList[i][j]

tempLabelList = [[finalList[-1].copy()] for _ in range(len(finalList)-1)]

gini, split = [],  []   

r = finalList.copy()

for i in range(len(finalList) - 1):

	tempLabelList[i], r[i] =  sorting(finalList[i].copy(), tempLabelList[i][0])
	
	gini.append(gini_index(tempLabelList[i])[0])

	split.append(gini_index(tempLabelList[i])[1])

k = gini.index(min(gini)) 

s = r[k][split[k]]

dict = {'column k':k,'split s':s}

print(dict)