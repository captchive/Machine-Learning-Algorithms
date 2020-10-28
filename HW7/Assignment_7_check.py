
import sys
import random
import math

### Read Data #
f = open(sys.argv[1])
data = []
l = f.readline()
while (l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
datarows = len(data)
datacols = len(data[0])
f.close()

### Read Training #

trainlabels = {}
f = open(sys.argv[2])
l = f.readline()
nclass = []
nclass.append(0)
nclass.append(0)
while (l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    nclass[int(a[0])] = nclass[int(a[0])] + 1
    l = f.readline()
f.close()


def boot_strap(trainlabels, data, datarows, datacols):
    nkey = list()
    sdata = []
    strainlabels = {}
    for i in trainlabels.keys():
        nkey.append(i)
    # while (i != trainlabels.keys())
    #    nkey.append(i)

    # print(len(nkey))
    for i in range(0, len(nkey), 1):
        selectrows = random.choice(nkey)
        sdata.append(data[selectrows])
        strainlabels[i] = trainlabels.get(selectrows)
    # for i in range (0,datarows,1):
        # if (trainlabels.get(i) == None):
            # sdata.append(data[i])

    drows = len(sdata)
    dcols = len(sdata[0])
    return (sdata, strainlabels, drows, dcols)

def gini_cal(data,trainlabels,datarows,datacols,predict_v,r_ori,c_ori,mtrainlabels,mdata):
    ginivals = []
    split = 0
    l3 = [0, 0]
    for j in range(0, datacols, 1):
        ginivals.append(l3)
    temp = 0
    col = 0

    for j in range(0, datacols, 1):

        listcol = [item[j] for item in data]
        keys = sorted(range(len(listcol)), key=lambda k: listcol[k])
        listcol.sort()
        # print("sorted list",listcol)
        # print("keys ",keys)
        ginival = []
        prevgini = 0
        prevrow = 0
        for k in range(1, datarows, 1):

            lsize = k
            rsize = datarows - k
            lp = 0
            rp = 0

            for l in range(0, k, 1):
                if (trainlabels[keys[l]] == 0):
                    lp += 1
            for r in range(k, datarows, 1):
                if (trainlabels[keys[r]] == 0):
                    rp += 1
                    # print(lp,",",rp)
                    # if(k!=1 and prevrow==listcol[k]):
                    #   gini = min(ginival)
                    #   continue
            gini = (lsize / datarows) * (lp / lsize) * (1 - lp / lsize) + (rsize / datarows) * (rp / rsize) * (
                1 - rp / rsize)
            # print(gini)
            ginival.append(gini)

            prevgini = min(ginival)
            # print("k-1",k-1)
            if (ginival[k - 1] == float(prevgini)):
                ginivals[j][0] = ginival[k - 1]
                ginivals[j][1] = k
        # print(ginival, ginivals[j][1], ginivals[j][0])
        # print(ginivals)
        # ginimini=min(ginival)
        if (j == 0):
            temp = ginivals[j][0]
            # print("temp",temp)
        if (ginivals[j][0] <= temp):
            temp = ginivals[j][0]
            col = j
            split = ginivals[j][1]
            # print("split",split)
            if (split != 0):
                split = (listcol[split] + listcol[split - 1]) / 2
    print("gini:", temp, "col:", col, "split:", split)

    var = 0
    m = 0
    p = 0
    for i in range(0, r_ori, 1):
        if (mtrainlabels.get(i) != None):
            if (mdata[i][col] < split):
                if (mtrainlabels.get(i) == 0):
                    m += 1
                if (mtrainlabels.get(i) == 1):
                    p += 1
    if (m > p):
        left = 0
        right = 1
    else:
        left = 1
        right = 0

    for i in range(0, r_ori, 1):
        if (mtrainlabels.get(i) == None):
            if (mdata[i][col] < split):
                var = left
            else:
                var = right

            if i in predict_v:
                predict_v[i].append(var)
            else:
                predict_v[i] = [var]

    return (predict_v)



predict_v = dict()
r_ori = len(data)
c_ori = len(data)
mdata = data
mtrainlabels = trainlabels

for i in range(0, 100, 1):
    # sdata,strainlabels,drows,dcols = boot_strap(trainlabels,data)
    sdata, strainlabels, drows, dcols = boot_strap(trainlabels, data, datarows, datacols)
    # predict_v = gini_cal(trainlabels,data,drows,dcols,predict_v)
    predict_v = gini_cal(sdata, strainlabels, drows, dcols, predict_v, r_ori, c_ori, mtrainlabels, mdata)
    #print (predict_v)


for k, v in predict_v.items():
    ct = sum(predict_v[k])
    if ct > 50:
        predict_v[k]=1
    else:
        predict_v[k]=0
    print(predict_v[k], k)