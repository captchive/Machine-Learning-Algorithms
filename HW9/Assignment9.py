import sys
from sklearn.svm import LinearSVC
from sklearn import svm
import random
from sklearn.model_selection import KFold

def dot(w, data):
    dp = 0
    for j in range (0, cols, 1):
        dp = dp + (w[j] * data[j])
    return dp


def sign(x):
    if x > 0:
        return 1.
    elif x < 0:
        return -1.
    elif x == 0:
        return 0.
    else:
        return x

def getbestC(train,labels):
               
        random.seed()
        allCs = [.001, .01, .1, 1, 10, 100]
        error = {}
        for j in range(0, len(allCs), 1):
                error[allCs[j]] = 0
        rowIDs = []
        for i in range(0, len(train), 1):
                rowIDs.append(i)
        nsplits = 1
        for j in range(len(allCs)):        
                #### Making a random train/validation split of ratio 90:10
                newtrain = []
                newlabels = []
                validation = []
                validationlabels = []

                random.shuffle(rowIDs) #randomly reorder the row numbers      
                #print(rowIDs)

                for i in range(0, int(.9*len(rowIDs)), 1):
                        newtrain.append(train[i])
                        newlabels.append(labels[i])
                for i in range(int(.9*len(rowIDs)), len(rowIDs), 1):
                        validation.append(train[i])
                        validationlabels.append(labels[i])
               # print(newtrain[0])
                #### Predict with SVM linear kernel for values of C={.001, .01, .1, 1, 10, 100} ###
                kf = KFold(n_splits=5,shuffle=True)
                
                
                
                for train_index, test_index in kf.split(train):
                        newtrain,validation = [train[i1] for i1 in train_index], [train[i2] for i2 in test_index]
                        newlabels,validationlabels = [labels[i1] for i1 in train_index], [labels[i2] for i2 in test_index]
                        
                        C = allCs[j]
                        clf = svm.LinearSVC(C=C,max_iter=10000)
                        clf.fit(newtrain, newlabels)
                        prediction = clf.predict(validation)
                        #print(clf.score(validation,validationlabels))
                        err = 0
                        for i in range(0, len(prediction), 1):
                                if(prediction[i] != validationlabels[i]):
                                        err = err + 1
                        #print('>>',error)
                        err = err/len(validationlabels)
                        error[C]=err
        #print(error)


        bestC = 0
        minerror=100
        keys = list(error.keys())
        for i in range(0, len(keys), 1):
                key = keys[i]
                error[key] = error[key]/nsplits
                if(error[key] < minerror):
                        minerror = error[key]
                        bestC = key

        #print(bestC,minerror)
        return [bestC,minerror,prediction]

# Read data from file
#f = open('data.txt')

datafile = sys.argv[1]
f = open(datafile)

data = []
l = f.readline()
while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
#    l2.append(float(1))
    data.append(l2)
    l = f.readline()

rows = len(data)
cols = len(data[0])


# Read labels from file
#f = open('labels.txt')
labelsfile = sys.argv[2]
f = open(labelsfile)
train_labels = {}
n = []
n.append(0)
n.append(0)
l = f.readline()
while (l != ''):
    a = l.split()
    train_labels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] +=1

 ###############################################################
X=[]
Labels=[]
for i in range(0,rows,1):
    if train_labels.get(i) != None:
        X.append(data[i])
        Labels.append(train_labels.get(i))
X_train=[]
X_test=[]
X_trainlabels=[]
X_testlabels=[]        
#print(Labels[0])
for i in range(0,int(0.8*len(X)),1):
    X_train.append(X[i])
    X_trainlabels.append(Labels[i])
for i in range(int(0.8*len(X)),len(X),1):
    X_test.append(X[i])
    X_testlabels.append(Labels[i])
   
[bestC,minerror,prediction]=getbestC(X,Labels)

clf = LinearSVC(C=bestC,max_iter=10000)
clf.fit(X_train, X_trainlabels)
prediction = clf.predict(X_test)
print('>>>>>>',X_testlabels,prediction)
err = 0
for i in range(0, len(prediction), 1):
        if(prediction[i] != X_testlabels[i]):
                err = err + 1

err = err/len(X_testlabels)
print('bestC=',bestC,'minerror',minerror,"best error=",err)