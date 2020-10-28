import sys
import math
import random

#Read Data File
datafile =sys.argv[1]

f = open (datafile,'r')
data = []
l = f.readline()
while(l !=''):
    a = l.split()
    l2 = [1]
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()

rows = len (data)
cols = len (data[0])
f.close()

#print (data)
#Read Label File

labelfile=sys.argv[2]
f = open (labelfile,'r')
trainlabels = {}
n = [0,0]
l=f.readline()
while(l != ''):
    a =(l.split())
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] +=1

#Gini Values

gini_vals = []
split = 0
l3 = [0, 0]
for j in range(0, cols, 1):
    gini_vals.append(l3)
temp = 0
col = 0

for j in range(0, cols, 1):

    listcol = [item[j] for item in data]
    keys = sorted(range(len(listcol)), key=lambda k: listcol[k])
    listcol.sort()
    gini_val = []
    prev_gini = 0
    prevrow = 0
    for k in range(1, rows, 1):

        lsize = k
        rsize = rows - k
        lp = 0
        rp = 0

        for l in range(0, k, 1):
            if (trainlabels.get(l) == 0):
                lp += 1
        for r in range(k, rows, 1):
            if (trainlabels.get(r) == 0):
                rp += 1
                # print(lp,",",rp)
                # if(k!=1 and prevrow==listcol[k]):
                #   gini = min(gini_val)
        gini = (lsize / rows) * (lp / lsize) * (1 - lp / lsize) + (rsize / rows) * (rp / rsize) * (
            1 - rp / rsize)
        # print(gini)
        gini_val.append(gini)

        prev_gini = min(gini_val)
        # print("k-1",k-1)
        if (gini_val[k - 1] == float(prev_gini)):
            gini_vals[j][0] = gini_val[k - 1]
            gini_vals[j][1] = k
    # print(gini_val, gini_vals[j][1], gini_vals[j][0])
    # print(gini_vals)
    # gini_mini=min(gini_val)

    if (j == 0):
        temp = gini_vals[j][0]
        # print("temp",temp)

    if (gini_vals[j][0] <= temp):
        temp = gini_vals[j][0]
        col = j
        split = gini_vals[j][1]
        # print("split",split)
        if (split != 0):
            split = (listcol[split] + listcol[split - 1]) / 2
print("gini:", temp, "col:", col, "split:", split)
