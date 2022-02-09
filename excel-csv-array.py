# -*- coding:utf-8 -*-  

import csv
import numpy
file_name = "2015lb"
root_file = "E:\\MachineLearning-data\\"
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
        c=b[1:]
        a = row[1:-1]
        rows_data.append(a)
        rows_target.append(c)
with open(path_data,'w',newline='') as pd:
    writer = csv.writer(pd)
    m = len(rows_data)
    for i in range(m):
        if i > 0:
            writer.writerow(rows_data[i])
with open(path_target,'w',newline='') as pt:
    writer = csv.writer(pt)
    n = len(rows_target)
    for i in range(n):
        if i > 0:
            writer.writerow(rows_target[i])
data_matrix = numpy.loadtxt(path_data,delimiter=",")
target_matrix = numpy.loadtxt(path_target,delimiter=",")
data = numpy.array(data_matrix)
target = numpy.array(target_matrix)
print(str(data))
print(str(target))
print('success')