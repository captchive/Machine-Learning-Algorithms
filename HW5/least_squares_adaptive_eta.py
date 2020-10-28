import sys, random, datetime


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

	return lsi, lstrain, lstest


def dot(w, trainList):

	outPut = []

	for i in trainList:

		i = [1] + i

		sum = 0

		for j,k in zip(w, i):
			
			sum += j * k
		
		outPut.append(sum)
	
	return outPut


def max11(a, b):

	if a >= b:
		
		return a
	
	else:
	
		return b


def loss(outPut, trainList, w, alpha = 0.0001):

	totalLoss = [0 for _ in w]

	actual = [i[-1] for i in trainList]
	
	ActualLoss = 0
	
	temp = [i * j for i, j in zip(outPut, actual)]

	for n, i, j in zip(temp, trainList, outPut):
	
		i = [1] + i
		
		for k in range(len(w)): 
			
			if n < 1:
		
				totalLoss[k] += (alpha * i[-1] * (i[k]))
			
			else:
				
				totalLoss[k] += 0
			
		ActualLoss += max11(0, 1 - n)
	
	return totalLoss, ActualLoss


def HingeLoss(trainList,pow=0.001, alpha = 0.001):

	if len(sys.argv) >= 4:

		alpha = float(sys.argv[3])

	if len(sys.argv) == 5:
	
		pow = float(sys.argv[4])

	weightList, hle, i, alpha =[random.random() for _ in range(len(trainList[0]))], [2, 1, 1], 1, []
	
	tempWeightList = weightList.copy()
	
	for _ in range(10):
		
		alpha.append(i)
		
		i /= 10
	now=datetime.datetime.now()
					
	while (abs(hle[1] - hle[0]) > pow):

		outPut = dot(weightList, trainList)
		
		#hle.pop()
		
		tempLoss = []	
		
		for ind in range(len(alpha)):
			
			tempWeightList = weightList.copy()

			for i in range(len(weightList)):
				
				tempWeightList[i] += loss(outPut, trainList, weightList,alpha =  alpha[ind])[0][i]

			tempLoss.append(loss(dot(tempWeightList, trainList), trainList, tempWeightList)[1])
			
			if tempLoss[ind] == min(tempLoss):
			
				tmpwght = tempWeightList 
		
		weightList = tmpwght
		
		hle = [min(tempLoss)] + hle

		print('loss>', hle[0], 'stopping threshold>', abs(hle[1]-hle[0]))
	then=datetime.datetime.now()
	print(then-now)
	return weightList


#opening files
inputList = getFeatureData(sys.argv[1])

labelList = getLabelData(sys.argv[2])


tsl = []

for k, v in labelList.items():
	
	tsl.append([v,k])

labelList = tsl

features = (len(inputList[0]))


#replacing 0 with -1 for classification
for n, i in enumerate(labelList):
	
	if i[0] == 0:
		
		labelList[n][0] = -1
	else:
		i[0] = 1

#connecting missing labels with it's features
inputList, trainList, testList = connectLabels(inputList, features, labelList)

for i in range(len(inputList)):	

	inputList[i] = [1] + inputList[i]

#training
w = HingeLoss(trainList)

#classifying regression labels with boundry conditions
for n, i in enumerate(testList):
	
	sum = 0

	i = [1] + i
	
	for k, j in zip(w,i):
		
		sum += k * j
	
	if sum > 0:
	
		sum = 1
	
	else:
		
		sum = 0
	
	testList[n].append(sum)

for n, i in enumerate(inputList):

	for j in testList:

		if i[1:] == j[:len(j)-1]:
		
			print(j[-1], n)

w0 = w.pop(0)

sum = 0

for i in w:

	sum += i ** 2

print("weights:", w)

print("distance of plane from origin:", w0/ (sum) ** (1 / 2))