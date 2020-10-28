import random , sys 
from sklearn.svm import LinearSVC
from sklearn import svm

#from sklearn.metrics import confusion_matrix
#importing datasets
input_file = sys.argv[1]
data_labels = sys.argv[2]
try:
    test = data_labels.replace('.trainlabels.0', '.labels')                                                                                                       
except:
    print("please enter .label file through command line")
    test = sys.argv[4]   
level_k = 10000

def getbestC(train,labels):
        random.seed()
        allCs = [.001, .01, .1, 1, 10, 100]
        error = {}
        for j in range(0, len(allCs), 1):
                error[allCs[j]] = 0
        rowIDs = []
        for i in range(0, len(train), 1):
                rowIDs.append(i)
        nsplits = 10
        for x in range(0,nsplits,1):        
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
                #### Predict with SVM linear kernel for values of C={.001, .01, .1, 1, 10, 100} ###
                
            for j in range(0, len(allCs), 1):
                C = allCs[j]
                clf = svm.LinearSVC(max_iter = 10000)
                clf.fit(newtrain, newlabels)
                prediction = clf.predict(validation)
                err = 0
                for i in range(0, len(prediction), 1):
                    if(prediction[i] != validationlabels[i]):
                        err = err + 1
                        err = err/len(validationlabels)
                        error[C]+=err
                        #print("err=",err,"C=",C,"split=",x)
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
        return [bestC,minerror]
   
#dotproduct function
def dot(X,Y):
    a=0
    for i in range(len(X)):
        a=a+(X[i]*Y[i])
    return a

#getting the features
with open (input_file) as f:
    feature = [[float(x) for x in line.split()] for line in f]
f.close()

#reading the labels
f1= open(data_labels)
datalabels = {}
for line in f1:
    row = line.split()
    datalabels[int(row[1])] = int(row[0])
f1.close()

#changing labels from 0 to -1.
for key in datalabels:
    value = datalabels[key]
    if value==0:
        datalabels[key]= -1

#reading the test labels
f1= open(test)
testlab = {}
for line in f1:
    row = line.split()
    testlab[int(row[1])] = int(row[0])
f1.close()

y_true =[]
for i in range(len(testlab)):
    if(datalabels.get(i)==None):
        y_true.append(testlab[i])

z =  [0 for _ in range(int(level_k))]
#let z and z1 be the empty list initially
for k in range(int(level_k)):
    w=[]       
    w = [random.uniform(-1,1) for _ in range(len(feature[0]))]
    temp =[]
    for i in range(len(feature)):
        temp.append(dot(feature[i], w))
    min_w = min(temp)
    max_w = max(temp)
    w0 = random.uniform(min_w , max_w)
    z1=[]
    for i in range(len(feature)):
            #store=0
        store = (dot(feature[i],w) + w0)
        if (store < 0):
            store = -1
        else:
            store = 1
        z1.append(store)
    z[k] = z1
    
z_trans = []
for i in range(len(z[0])):
    row =[] 
    for item in z: 
        row.append(item[i]) 
    z_trans.append(row)    
    
z_training_data = [ ]
for i in range(len(z_trans)):
    if(datalabels.get(i)!=None):
        z_training_data.append(z_trans[i])
    
#labels to list    
lab = []
for i in range(len(z_trans)):
    if(datalabels.get(i)!=None):
        lab.append(datalabels.get(i))

testing_data = []
for i in range(len(z_trans)):
    if(datalabels.get(i)==None):
        testing_data.append(z_trans[i])

#trainlabels to list
trainlabels = []
for i in range(len(z_trans)):
    if(datalabels.get(i)!=None):
        trainlabels.append(feature[i])

#testlabels list
test_labels = []
for i in range(len(z_trans)):
    if(datalabels.get(i)==None):
        test_labels.append(feature[i])

index= []
for i in range(len(feature)):
    if(datalabels.get(i)==None):
        index.append(i)

bestc , minerror = getbestC(trainlabels , lab)
#Run linear SVM on Z and predict on Z1.    
svc=LinearSVC(C = bestc , max_iter = 10000)
svc.fit(trainlabels , lab)
pred = svc.predict(test_labels)

for i in range(len(pred)):
    if(pred[i] == -1):
        pred[i]=0

count = 0   
for i in range(len(pred)):
    if(pred[i]!= y_true[i]):
        count+=1
testerror = (count / (len(pred)))*100
#print("testerror :" ,testerror)
print("Original data :Linear SVC best C : " +str(bestc)+ " , best CV error : " +  str(minerror*100)+"% , testerror :" +str(testerror))

#Run linear SVM on Z and predict on Z1.    
svc=LinearSVC(C = bestc , max_iter = 10000)
svc.fit(z_training_data , lab)
pred = svc.predict(testing_data)

count = 0   
for i in range(len(pred)):
    if(pred[i]!= y_true[i]):
        count+=1
testerror1 =(count / (len(pred)))*100
#print("testerror :" ,testerror1)
#print(pred)
new = getbestC(z_training_data , lab)      
print("new data :Linear SVC best C : " +str(new[0])+ " , best CV error : " + str(new[1]*100)+"% , testerror :" +str(testerror1))
for i in range(len(pred)):
    if(pred[i] == -1):
        pred[i] =0
    print(pred[i] , index[i])
    




    

