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
def sorting(featuresList,labelsList):
	n, tempL = len(featuresList), []
	for i in range(n):
		tempL.append(labelsList[featuresList.index(min(featuresList))])
		
		labelsList.pop(featuresList.index(min(featuresList)))
		featuresList.pop(featuresList.index(min(featuresList)))

	return tempL
def gini_index(tempLableList,l_l):
	minimum = 10000000
	split = 0	
	#print(tempLableList)
	for j in range(1,len(tempLableList)-1,1):
		

		L_S,R_S = tempLableList[:j],tempLableList[j:]
		ans = ((j/len(tempLableList))*(L_S.count(0)/j)*(1-L_S.count(0)/j))+(((len(tempLableList)-j)/len(tempLableList))*(R_S.count(0)/(len(tempLableList)-j))*(1-R_S.count(0)/(len(tempLableList)-j)))
		#print(L_S.count(1),R_S.count(1))
		if ans<minimum:
			minimum = ans
			split = j
		#print(minimum,split)
	return minimum,split
#opening files
inputList = getFeatureData(sys.argv[1])

labelList = getLabelData(sys.argv[2])


labelList = [[v, k] for k,v in labelList.items()]


#connecting missing labels with it's features
trainList, testList = connectLabels(inputList, len(inputList[0]), labelList)
finalList=[[0 for _ in trainList] for _ in range(len(trainList[0]))]

for i in range(len(trainList)):
		for j in range(len(trainList[0])):
			finalList[j][i] = trainList[i][j]

tempLabelList = [finalList[-1].copy() for _ in range(len(finalList)-1)]
#print(tempLabelList,'<<')
gini,split=[],[]
for i in range(len(finalList)-1):
	#print(tempLabelList[i],i)
	tempLabelList[i] =  sorting(finalList[i].copy(),tempLabelList[i][0])
	if tempLabelList[i][:int(len(tempLabelList[i])/2)].count(0)>tempLabelList[i][:int(len(tempLabelList[i])/2)].count(1):
		l_l = 0
		r_l = 1
	else:
		l_l = 1
		r_l =0
	
	gini.append(gini_index(tempLabelList[i],l_l)[0])
	split.append(gini_index(tempLabelList[i],l_l)[1])
print(gini,split)
k = gini.index(min(gini))+1
s = finalList[k][split[k]]
#print('for column {}, gini index is lowest ({}) with condition "if s < {} ans = {} else ans = {}"'.format(k,gini[k],s,l_l,r_l))
print("coloumn number k = {} gives best split on s = {}".format(k,s))