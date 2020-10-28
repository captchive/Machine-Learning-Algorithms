#LOADING THE DATASET
import sys, math, random

input_file = sys.argv[1]

label_file = sys.argv[2]

#reading the feature file
with open (input_file) as f:
    
    feature = [[float(x) for x in line.split()] for line in f]

f.close()
 
#reading the labels
f1 = open(label_file)

datalabels = {}

for line in f1:

    row = line.split()

    datalabels[int(row[1])] = int(row[0])

f1.close()

#initialising the eta, preverror, and stopping condition
lr = 0.01

stopping_condition = 0.0000001

preverror=10000

#defining the sigmoid function
def sigmoid(z):

    sig = []

    for i in z:

        if i < -10:

            sig.append(0.00001)

        elif 1 / (1 + math.exp(-i)) == 1:

            sig.append(0.99999)

        else:

            sig.append(1 / (1 + math.exp(-i)))

    return sig


#defining t	he loss function
def loss(h, y):

    a = 0
	
    for i in range(len(h)):

        a -= (y.get(i) * math.log(h[i]) + (1 - y.get(i)) * math.log(1 - h[i]))

    return a


#defining dot product of the feature and weight
def dot(X, Y):

    dot1 = []

    for i, n in enumerate(X):

        n = [1] + n

        sum = 0

        for j in range(len(Y)):

            sum += (n[j] * Y[j])

        dot1.append(sum)

    return dot1


#prediction function
def predict_prob(X):    

        return sigmoid(dot(X, theta))


#initializing the weights
theta = [random.uniform(0, 1) for _ in range(len(feature[0]) + 1)]

#computing and updating the weights
diff = []

while(1):

    h,error = sigmoid(dot(feature,theta)), loss(sigmoid(dot(feature,theta)), datalabels)

    for i, n in enumerate(feature):

        n = [1] + n

        for j in range(len(feature[0])):

            theta[j] += (lr * n[j] * (datalabels[i] - h[i]))
	
    if(abs(preverror - error) <= stopping_condition):

        break
 	
    preverror = error
      
#for the distance W:
theta0 = theta.pop(0)

print("theta0: ", theta0,theta)

a = 0

for i in range(len(theta)):

    a += theta[i] ** 2

denominator = math.sqrt(abs(a))

distance = (theta0 / denominator)

print("distance to origin :", distance)

#prediction#ignore
#a=predict_prob(x)

#if(a < 0.5):

#    print("0")

#else:
 
#    print("1")

            
            
    
    
    
    
    