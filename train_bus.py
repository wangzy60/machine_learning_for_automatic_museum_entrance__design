# -*- coding:utf-8 -*-  
import numpy as np 
import csv
from sklearn.metrics import confusion_matrix, classification_report 
from sklearn.preprocessing import LabelBinarizer 
from NeuralNetwork import NeuralNetwork
from sklearn.cross_validation import train_test_split
############################################
file_name = "2015library_buspower"
root_file = "E:\\MachineLearning-data\\BusStation\\"
end_formual = ".csv"
path_old = root_file + file_name + end_formual  
path_data = root_file + file_name + '_data' +  end_formual
path_target = root_file + file_name + '_target' +  end_formual
with open(path_old,'r') as f:
    reader = csv.reader(f)
    rows_data = []
    rows_target = []
    for row in reader:
        tem = row[-1]
        b = str(tem).split('：')
        c=b[-1]
        a = row[1:-1]
        rows_data.append(a)
        rows_target.append(c)
with open(path_data,'w',newline='') as pd:
    writer = csv.writer(pd)
    print(rows_data)
    m = len(rows_data)
    for i in range(m):
        if i > 0:
            writer.writerow(rows_data[i])
with open(path_target,'w',newline='') as pt:
    writer = csv.writer(pt)
    print(rows_target)
    n = len(rows_target)
    for i in range(n):
        if i > 0:
            writer.writerow(rows_target[i])
data_matrix = np.loadtxt(path_data,delimiter=",")
target_matrix = np.loadtxt(path_target,delimiter=",")
data = np.array(data_matrix)
target = np.array(target_matrix)
#print(data)
#print(target)
########################################
X = data  
y = target
X -= X.min() # normalize the values to bring them into the range 0-1  
X /= X.max()
#print(X)
nn = NeuralNetwork([16,35,4],'logistic')  
X_train, X_test, y_train, y_test = train_test_split(X, y)
labels_train = LabelBinarizer().fit_transform(y_train)
labels_test = LabelBinarizer().fit_transform(y_test)
print("start fitting")
nn.fit(X_train,labels_train,epochs=50000)  
predictions = []  
for i in range(X_test.shape[0]):  
    o = nn.predict(X_test[i] )  
    predictions.append(np.argmax(o))  
print(confusion_matrix(y_test,predictions))  
print(classification_report(y_test,predictions))
