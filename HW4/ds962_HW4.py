import sys, random, math



def getFeatureData(featureFile, bias = 0):
	
	x = []
	
	dFile = open(featureFile, 'r')
	
	i = 0
	
	for line in dFile:
	
		row = line.split()
		
		rVec = [float(item) for item in row]
		
		if bias > 0:
		
			rVec.insert(0, bias)

#		print('row {} : {}'.format(i,rVec))
 
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
	
	print('label : {}'.format(lDict))
		
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


def sigmoid(weightList, trainList):
	
	outPut = dot(weightList, trainList)
	
	for i in range(len(outPut)):

		#if outPut[i] > -3:
			
		outPut[i] = 1 / (1 + (2.718281828459045) ** (-1 * outPut[i]))
		
		#else:
		
		#	outPut[i] = 0
	
	return outPut

def sigm (w, inp):

	sum = 0

	for i in range(len(w)):
		
		sum += w[i] * inp[i]

	sum = 1/(1+ (2.718281828459045 ** (-1*sum)))

	if sum == 1.0:
	
		sum = 0.9999
	
	return sum


def loss(outPut, trainList, weightList, alpha = 0.001):
	#print()
	totalLoss = [0 for _ in weightList]

	lse = 0
	
	for  i, j in zip(trainList, outPut):
	
		i = [1] + i
		
		for k in range(len(weightList)):
			
			totalLoss[k] += (alpha * (i[-1] - j) * i[k])
			
		lse -=  (i[-1] * math.log(sigm(weightList, i)) + ((1 - i[-1]) * math.log(1 - sigm(weightList, i))))

	return totalLoss, lse


def logisticRegression(trainList,pow=0.001, alpha = 0.001):
	
	if len(sys.argv) >= 4:

		alpha = float(sys.argv[3])

	if len(sys.argv) == 5:
	
		pow = float(sys.argv[4])
		
	weightList, lse, nofeatures, diff =[], 0, len(trainList[0]), 10
	
	for _ in range(nofeatures):
			
		weightList.append(random.random())

	while ( diff > pow):
		 
		outPut, prev, lse = sigmoid(weightList, trainList),lse, 0
	
		difw, lse = loss(outPut, trainList, weightList,alpha=alpha)
		
		for i in range(nofeatures):			
			
			weightList[i] += difw[i]
		
		diff = abs(prev - lse)
		
		print('\n>> error differnce =', diff, end = '')
	
	print(" FINAL LOSS =", lse)
	
	return weightList



#opening files
inputList = getFeatureData(sys.argv[1])

labelList = getLabelData(sys.argv[2])


tsl = []

for k, v in labelList.items():
	
	tsl.append([v,k])

labelList = tsl

features = (len(inputList[0]))


#connecting missing labels with it's features
inputList, trainList, testList = connectLabels(inputList, features, labelList)

for i in range(len(inputList)):	

	inputList[i] = [1] + inputList[i]

#training
w = logisticRegression(trainList)

#classifying regression labels with boundry conditions
for n, i in enumerate(testList):
	
	i = [1] + i

	sum = sigm(w,i)
		
	if sum > 0.5:

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

print("w =", w)

print("||w|| =", sum**(1/2))

print("distance from origin =", w0  / (sum) ** (1 / 2))
