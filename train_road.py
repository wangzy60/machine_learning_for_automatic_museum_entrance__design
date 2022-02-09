# -*- coding:utf-8 -*-  
import numpy as np 
import csv
from sklearn.metrics import confusion_matrix, classification_report ,precision_score,recall_score
from sklearn.preprocessing import LabelBinarizer 
from NeuralNetwork import NeuralNetwork
from sklearn.cross_validation import train_test_split
from mpl_toolkits.mplot3d import axes3d 
import matplotlib.pyplot as plt
from matplotlib import style
############################################
file_name = "2015library_list"
root_file = "E:\\MachineLearning-data\\Roads\\"
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
result_list = []
precision_list =[]
nn = NeuralNetwork([8,26,4],'logistic')  
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.2,random_state = 1)
labels_train = LabelBinarizer().fit_transform(y_train)
labels_test = LabelBinarizer().fit_transform(y_test)
print("start fitting")

nn.fit(X_train,labels_train,learning_rate=0.2,epochs=50000)  
predictions = []  
max_str = []
for i in range(X_test.shape[0]):  
    o = nn.predict(X_test[i] )  
    predictions.append(np.argmax(o))  
#print(classification_report(y_test,predictions))
precs = precision_score(y_test,predictions,average='weighted')
print(precs)

#
number_list = []
for i in range(len(predictions)):
    number_list.append(i)
###
style.use('grayscale')

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

x = y_test.tolist()
y = predictions
z = number_list
print(x)
print(y)
print(z)

x1 = []
y1 = []
z1 = []
x2 = []
y2 = []
z2 = []

for i in range(len(x)):
    if x[i] == y[i]:
        x1.append(x[i])
        y1.append(y[i])
        z1.append(i)
    elif x[i] != y[i]:
        x2.append(x[i])
        y2.append(y[i])
        z2.append(i)

ax1.scatter(x1, y1, z1, c='b', marker='o')
ax1.scatter(x2, y2, z2, c='y', marker='o')

ax1.set_xlabel('Actual Values')
ax1.set_xticks([0,1,2,3])
ax1.set_ylabel('Predicted Values')
ax1.set_yticks([0,1,2,3])
ax1.set_zlabel('Times')
ax1.set_zticks([0,10,20,30,40,50,60,70,80,90])

ax = plt.gca() # 获取当前的axes
ax.spines['right'].set_color('blue')
ax.spines['top'].set_color('grey')

 
plt.show()
 
print('done')
# with open(r'E:\max_road_finall.csv','w',newline='') as f:
#     writer = csv.writer(f,delimiter = ',')
#     for i in range(len(result_list)):
#         writer.writerow (result_list[i])
# print("down")
