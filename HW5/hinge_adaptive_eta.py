import sys , random, datetime

'''Get feature data from file as a matrix with a row per data instance'''
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


'''Get label data from file as a dictionary with key as data instance indexand value as the class index'''
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

def normalized(inputList):
	mean,std,n=[0 for _ in inputList[0]],[1 for _ in inputList[0]],len(inputList)
	#print(inputList[0])
	for i in inputList:
		
		for ind, j in enumerate(i):
			
			mean[ind] += (1/n)*(j)
	for i in inputList:
		
		for ind, j in enumerate(i):
			std[ind] += (1/n)*(j-mean[ind])**2
	for ind,i in enumerate(inputList):
		
		for jnd, j in enumerate(i):
			
			inputList[ind][jnd] -= mean[jnd]
			inputList[ind][jnd] /= std[jnd]
	#print(inputList[0])
	return inputList

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


def dot(weightList, trainList):

	outPut = []

	for i in trainList:

		i = [1] + i

		sum = 0

		for j,k in zip(weightList, i):
			
			sum += j * k
		
		outPut.append(sum)
	
	return outPut


def loss(outPut, trainList, weightList):
	
	totalLoss = [0 for _ in weightList]
	
	ActualLoss = 0

	for i, j in zip(trainList, outPut):
		
		i = [1] + i
	
		for k in range(len(weightList)): 
		
			totalLoss[k] += ((i[-1] - j) * i[k])
			
			ActualLoss += (1 / (2 * n)) * ((i[-1] - j) ** 2)
	
	return totalLoss,ActualLoss


def LeastSquare(trainList, pow = 0.001):
	
	if len(sys.argv) >= 4:

		alpha = float(sys.argv[3])

	if len(sys.argv) == 5:
	
		pow = float(sys.argv[4])
	
	weightList, lse, alphas, i =[0.002*random.random()-0.001 for _ in range(len(trainList[0]))], [2, 1, 2], [], 1
	
	tempWeightList =weightList.copy()
	
	for _ in range(10):
		
		alphas.append(i)
		
		i /= 10
	now=datetime.datetime.now()
	while (abs(lse[1] - lse[0]) > pow):

		outPut = dot(weightList, trainList)

		#lse.pop()
	
		tempLoss = []
		
		for ind,alpha in enumerate(alphas):
		
			tempWeightList = weightList.copy()
			
			for i in range(len(trainList[0])):
				
				tempWeightList[i] += alpha * (1 / (len(trainList) - 1)) * loss(outPut, trainList, weightList)[0][i]
			
			tempLoss.append(loss(dot(tempWeightList, trainList), trainList, tempWeightList)[1])
					
			if tempLoss[ind] == min(tempLoss):
				
				tmpwght = tempWeightList 
		
		weightList = tmpwght
	
		lse = [min(tempLoss)] + lse
		
		#previous error - current error
		print('loss>',lse[0],'stopping threshold>',lse[1]-lse[0])
	then=datetime.datetime.now()
	#print(then-now)
	return weightList

#opening files
inputList = getFeatureData(sys.argv[1])
inputList = normalized(inputList)
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
w = LeastSquare(trainList)


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

#print("weights:", w)

#print("distance of plane from origin:", w0 / (sum) ** (1 / 2))