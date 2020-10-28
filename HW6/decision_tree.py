import sys
import math
import random

#importing the data
input_file=sys.argv[1]
data_labels=sys.argv[2]

#reading the features 
with open (input_file) as f:
    feature = [[float(x) for x in line.split()] for line in f]
f.close()
#print(len(feature))
#reading the labels
datalabels = []
f1= open(data_labels)
for line in f1:
    row = line.split()
    datalabels.append([int(row[0]),int(row[1])])
f1.close()

#changing labels from 0 to -1.
for n,key in enumerate(datalabels):
    if key[0]==0:
        datalabels[n][0]= -1
    
def connectLabels(lsi, lsl):
	
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
def sortingfunction(data,labels):
	tem_data, c, temp_lab = [], len(data), []
	for _ in range(c):
		tem_data.append(min(data))
		temp_lab.append(labels[data.index(min(data))])
		labels.pop(data.index(min(data)))
		data.pop(data.index(min(data)))
	
	return tem_data,temp_lab
def split_gini(X,Y,l_l):
#this function splits the col values assuming that they are 
#already sorted and calculates the gini value for them.
    gini=[]
    rows=len(Y)
    #temp=[]
    #temp.clear()
#    print('{{{{{{{[',X)
    for i in range(1,len(Y),1):        
        left, right = Y[:i],Y[i:]
		
        lsize=len(left)
        rsize=len(right)
        lp = Y[:i].count(l_l)
        rp = Y[i:].count(l_l)
        gini.append((lsize/rows)*(lp/lsize)*(1 - (lp/lsize)) + (rsize/rows)*(rp/rsize)*(1 - (rp/rsize)))
    #print(min(gini))
    
    return gini.index(min(gini)),min(gini)

#spliting the column
known_data,unknown_data=connectLabels(feature,datalabels)
#print(len(known_data)+len(unknown_data))
a=[]
labels=[]
final_list=[]
b=[]
temp_tra = [[]for _ in range(len(known_data[0]))]
#print(known_data)
for i in range(len(known_data)):
    for j in range(len(known_data[0])):
        temp_tra[j].append(known_data[i][j])
#print(temp_tra)
for i in range(len(known_data[0])-1):
    sort_col, sort_labels= sortingfunction(temp_tra[i].copy(), temp_tra[-1].copy())
    #print(sort_col,sort_labels)
    if sum(sort_labels[:int(len(sort_labels)/2)])>0:
       l_l = 1
    else:
       l_l = -1
    #print(l_l)
    a.append(split_gini(sort_col, sort_labels,l_l)[1])
    b.append(sort_col[split_gini(sort_col, sort_labels,l_l)[0]])
    #col.clear()
#print(a)
k=a.index(min(a))
s=b[a.index(min(a))]
print("the column k is :",k, " and the split is at :",s)



         
      
    




