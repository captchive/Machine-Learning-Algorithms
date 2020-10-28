import sys, random, os

from collections import Counter
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


def euc_dist(ls1,ls2):

	dist = 0

	for i in range(len(ls1)):

		dist += abs(ls1[i] - ls2[i])

	return(dist)


def meaned(clusters):

	for cluster_num,cluster in clusters.items():
		
		meant = [0 for _ in cluster[0]]
		
		for m, row in enumerate(clusters[cluster_num][1]):
			
			for i in range(len(row)):   
				
				meant[i] += ((1/len(clusters[cluster_num][1]))* row[i])

		clusters[cluster_num][0] = meant

	return clusters



def KNN(inputList,k):

	cluster_key=[i for i in range(k)]

	clusters,dist,prev,error={},[],1500000,1450000

	for clu in cluster_key:

		clusters[clu] =[[clu for i in range(len(inputList[0]))],[]]

		dist.append(0)
	intial = True
	while(True):
		
		#Find the distance
		for key,value in clusters.items():

			clusters[key][1]=[]

		for n,i in enumerate(inputList):
			
			for key,value in clusters.items():	
				
				dist[key] = euc_dist(clusters[key][0], i)

			clusters[dist.index(min(dist))][1].append(i)

		clusters = meaned(clusters)
		
		prev = error

		error = sum(dist)/len(dist)
		
		if prev - error<0.0000000001 and prev-error>=0:
			break
	 
	return clusters

	
def sorting(featuresList, labelsList):

	n, tempL, tempF = len(featuresList), [], []

	for i in range(n):
		
		x = min(featuresList)
		
		tempL.append(labelsList[featuresList.index(x)])

		tempF.append(x)
		
		labelsList.pop(featuresList.index(x))

		featuresList.pop(featuresList.index(x))

	return tempL, tempF

#opening files

inputList = getFeatureData(sys.argv[1])
k = int(sys.argv[2])
x,y,means=[],[],[]
clusters=KNN(inputList,k)
for i in range(k):
	means.append(clusters[i][0])
	for j in clusters[i][1]:
		x.append(inputList.index(j))
		y.append(i)

sorted_x = []
m = x.copy()
#print(y)
ax=[]
for _ in (m):
	sorted_x.append([y[x.index(min(x))],min(x)])
	ax.append(y.pop(x.index(min(x))))
	x.pop(x.index(min(x)))
#for i,j in sorted_x:
	#print(i,j)

ab = {}
ab = ab.fromkeys(Counter(ax).keys())
for key in ab.keys():
	ab[key] = []
for n,i in enumerate(ax):
	ab[i].append(n-1)
for i in ab.keys(): 
	#print()	
	#print('cluster'+str(i)+":",ab[i])
	print(means[i])
