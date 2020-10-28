import sys
'''Get feature data from file as a matrix with a row per data instance'''

def getFeatureData(featureFile,bias=0):
	x=[]
	dFile = open(featureFile, 'r')
	i=0
	for line in dFile:
		row = line.split()
		rVec = [float(item) for item in row]
		if bias > 0:
			rVec.insert(0,bias)        
	
		x.append(rVec)        
		i += 1    
	dFile.close()
	
	return x
'''Get label data from file as a dictionary with key as data instance indexand value as the class index'''

def getLabelData(labelFile,hyperPlaneClass=False):
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
'''def fileToList(inputF):

	count, ls, num = sum(1 for line in inputF), [], 0

	inputF.seek(0, 0)
	
	for _ in range(count):

		ls.append((inputF.readline()).replace(" \n","").split(" "))
		
		if num < (len(ls[-1])):
			
			num = len(ls[-1])
		
	return [[float(s) for s in sublist] for sublist in ls], num'''


def connectLabels(lsi,n,lsl):
	
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


def meanOfClass(ls):

	m = [0 for i in range(len(ls[0]))]

	for i in ls:

		for j in range(len(i)):
			
			m[j] += i[j]/len(ls)
	
	for i in range(len(m)):
		
		m[i] = round(m[i],3)

	return m


def varienceOfClass(data = [], mean = 0):
	ls, m = data, mean

	s = [0 for i in range(len(ls[0]))]

	for i in ls:

		for j in range(len(i)):
			
			s[j] += ((i[j]-m[j])**2)/len(ls)

	for i in range(len(s)):

		if s[i]==0:

			s[i]=1
		
	return s


def makingCopy(inputList):
	
	initialList = []

	for n,i in enumerate(inputList):

		initialList.append([])

		for j in i:

			initialList[n].append(j)
	
	return initialList
	

def naiveBayesClassifier(data = [], model = 0):

	loss, losslist = {}, ['feature'+str(int(i)) for i in range(len(data))]

	loss = loss.fromkeys(tuple(losslist))

	for i in loss.keys():

		loss[i] = []
	
		for _ in model.keys():

			loss[i].append(0)

	for n,k in enumerate(model.keys()):

		for i in data.keys():

			for j in range(len(data[i])):

				loss[i][n] += ((data[i][j]-model[k][0][j])/(model[k][1][j]))**2

	for k in loss.keys():

		for n,v in enumerate(loss[k]):

				if v == min(loss[k]):
				
					data[k].append(n)

	return data


def preprocessAndTrain():

	className, distrubutedData, tempDict, modelDict = [], {}, {}, {}
	
	templist = ['feature'+str(i) for i in range(len(testList)) ]

	tempDict = tempDict.fromkeys(tuple(templist))

	for i in range(len(testList)):

		tempDict['feature'+str(i)] = testList[i]

	classes = list({i[0] for i in labelList})

	for i in classes:

		className.append("class"+str(int(i)))

	distrubutedData = distrubutedData.fromkeys(tuple(className))

	for k in distrubutedData.keys():

		distrubutedData[k] = []
	
	for i in trainList:

		for k in distrubutedData.keys():
		
			if int(k[-1]) == int(i[-1]):

				distrubutedData[k].append(i[:len(i)-1])

	modelDict = modelDict.fromkeys(tuple(className))

	for k in modelDict.keys():

		modelDict[k] = []

	for k in modelDict.keys():

		modelDict[k].append(meanOfClass(distrubutedData[k]))

		modelDict[k].append(varienceOfClass(mean = modelDict[k][0], data = distrubutedData[k]))

	return tempDict, modelDict


def outPutWrite(data, initialList):

	for n,i in enumerate(initialList):

		for v in data.values():

			if v[:len(v)-1] == i:

				print(v[-1], n)



#opening files
inputList = getFeatureData(sys.argv[1])

labelList = getLabelData(sys.argv[2])

tsl = []

for k, v in labelList.items():
	
	tsl.append([v,k])

labelList = tsl

features = (len(inputList[0]))

#establishing relation between appropriate label and features and creating training list
inputList, trainList, testList = connectLabels(inputList, features, labelList)

#making copy of input list for obtaining missing label values in further
initialList = makingCopy(inputList)

testDict, modelDict = preprocessAndTrain()

data = naiveBayesClassifier(data = testDict, model = modelDict)

outPutWrite(data, initialList)