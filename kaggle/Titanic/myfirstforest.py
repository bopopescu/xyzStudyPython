# coding:utf-8
""" Writing my first randomforest code.
Author : AstroDave
Date : 23rd September 2012
Revised: 15 April 2014
please see packages.python.org/milk/randomforests.html for more

"""
import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

# 读取训练数据
train_df = pd.read_csv('train.csv', header=0)

# I need to convert all strings to integer classifiers.
# I need to fill in the missing values of the data and make it complete.

# 转换数据类型，女人0，男人1
# female = 0, Male = 1
train_df['Gender'] = train_df['Sex'].map({'female': 0, 'male': 1}).astype(int)
import pdb
pdb.set_trace()
# Embarked from 'C', 'Q', 'S'
# Note this is not ideal: in translating categories to numbers, Port "2" is not 2 times greater than Port "1", etc.

# All missing Embarked -> just make them embark from most common place
# train_df.Embarked 数据集中一个属性
# train_df.Embarked.isnull() 每一列是不是空数据列
# train_df.Embarked[train_df.Embarked.isnull()] 数据为空的列
if len(train_df.Embarked[train_df.Embarked.isnull()]) > 0:
    # 补充众数
    train_df.Embarked[train_df.Embarked.isnull()] = train_df.Embarked.dropna().mode().values

# 创建Embarked字典映射
Ports = list(enumerate(np.unique(train_df.Embarked)))  # determine all values of Embarked,
Ports_dict = {name: i for i, name in Ports}  # set up a dictionary in the form  Ports : index
train_df.Embarked = train_df.Embarked.map(lambda x: Ports_dict[x]).astype(int)  # Convert all Embark strings to int

# All the ages with no data -> make the median of all Ages
# 平均年龄
median_age = train_df.Age.dropna().median()
# 年龄中位数补充
if len(train_df.Age[train_df.Age.isnull()]) > 0:
    train_df.loc[(train_df.Age.isnull()), 'Age'] = median_age

# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
train_df = train_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1)

# TEST DATA
test_df = pd.read_csv('test.csv', header=0)  # Load the test file into a dataframe

# I need to do the same with the test data now, so that the columns are the same as the training data
# I need to convert all strings to integer classifiers:
# female = 0, Male = 1
test_df['Gender'] = test_df['Sex'].map({'female': 0, 'male': 1}).astype(int)

# Embarked from 'C', 'Q', 'S'
# All missing Embarked -> just make them embark from most common place
if len(test_df.Embarked[test_df.Embarked.isnull()]) > 0:
    test_df.Embarked[test_df.Embarked.isnull()] = test_df.Embarked.dropna().mode().values
# Again convert all Embarked strings to int
test_df.Embarked = test_df.Embarked.map(lambda x: Ports_dict[x]).astype(int)

# All the ages with no data -> make the median of all Ages
median_age = test_df['Age'].dropna().median()
if len(test_df.Age[test_df.Age.isnull()]) > 0:
    # loc通过行标签取得索引
    test_df.loc[(test_df.Age.isnull()), 'Age'] = median_age

# All the missing Fares -> assume median of their respective class
if len(test_df.Fare[test_df.Fare.isnull()]) > 0:
    median_fare = np.zeros(3)
    for f in range(0, 3):  # loop 0 to 2
        median_fare[f] = test_df[test_df.Pclass == f + 1]['Fare'].dropna().median()
    for f in range(0, 3):  # loop 0 to 2
        test_df.loc[(test_df.Fare.isnull()) & (test_df.Pclass == f + 1), 'Fare'] = median_fare[f]

# Collect the test data's PassengerIds before dropping it
ids = test_df['PassengerId'].values
# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
test_df = test_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1)

# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array
train_data = train_df.values
test_data = test_df.values

# 以上是通过pandas对数据进行清洗和整理，下面开始对数据进行训练

print 'Training...'
# n_estimators 树的个数
forest = RandomForestClassifier(n_estimators=100)
# fit第一个参数为样本，第二个参数为标签
forest = forest.fit(train_data[0::, 1::], train_data[0::, 0])

pdb.set_trace()

print 'Predicting...'
# test_data 训练数据
output = forest.predict(test_data).astype(int)

predictions_file = open("myfirstforest.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId", "Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'
