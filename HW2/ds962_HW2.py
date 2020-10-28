import sys


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

		#print('row {} : {}'.format(i,rVec))
 
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
			
			ActualLoss += (1 / (2)) * ((i[-1] - j) ** 2)
	
	return totalLoss,ActualLoss


def LeastSquare(trainList):

	weightList, lse, α, n =[], [2, 1, 1], 0.0001, len(trainList)
	
	for i in trainList:
	
		nofeatures = len(i)
	
	for j in range(nofeatures):
			
		weightList.append(1)
					
	while ((lse[0] - lse[2]) > 0.001 or (lse[0] - lse[2]) < -0.001):

		#updating learning rate dynamically as it varies with mathematical complexity of each dataset
#		if lse[0] / lse[2] > 10:
	
#			α = α / 10

		outPut = dot(weightList, trainList)

		lse.pop()

		for i in range(nofeatures):
		
			weightList[i] += α * (1 / (n-1)) * loss(outPut, trainList, weightList)[0][i]
			
		lse = [loss(outPut, trainList, weightList)[1]] + lse
		#previous error - current error
#		print(lse[2]-lse[0])

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
#print(trainList)

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

w0=w.pop(0)

sum=0

for i in w:

	sum+=i**2

print("weights:",w)

print("distance of plane from origin:",(w0**2)**(1/2)/(sum)**(1/2))
