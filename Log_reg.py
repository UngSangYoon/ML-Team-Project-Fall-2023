import numpy as np
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from embed_and_norm import *
x=[]
y=[]
x_test=[]
y_test=[]
for i in range(17):
    with open(f'dataset/{i+3:02d}_{i+4:02d}.json') as file:
        stat = json.load(file)
    with open(f'dataset/{i+3:02d}_{i+4:02d}_score.json') as file:
        score = json.load(file)
    x.extend(stat)
    y.extend(score)


x_train = x
x_train = np.array(x_train)
y_train = y
y_train = [(int(pair[0]),int(pair[1])) for pair in y_train]
y_train = [list(pair) for pair in y_train]
y_train = score_to_target(y_train)
#X_TEST/Y_TEST
with open('dataset/21_22.json') as file:
    stat = json.load(file)
with open('dataset/21_22_score.json') as file:
    score = json.load(file)
x_test.extend(stat)
y_test.extend(score)
y_copy = y_test
x_test = np.array(x_test)
y_test = score_to_target(y_test)

class LogisticRegression:
    def __init__(self, x_train, y_train, x_test, y_test):
        self._x_train = x_train
        self._y_train = y_train
        self._x_test = x_test
        self._y_test = y_test
        size_x = self._x_train.shape
        size_x = int(size_x[1])
        size_y = self._y_train.shape
        size_y = int(size_y[1])
        self.bias = np.zeros((size_x, size_y))

    def sigmoid(self, x, bias):
        return 1.0 / (1.0 + np.exp(-np.dot(x, bias)))

    def cost(self, x, y, bias):
        size = self._x_train.shape
        size = int(size[0])
        delta = 1e-10  # 무한대 방지
        h = self.sigmoid(x, bias)
        costs = y * np.log(h + delta) + (1 - y) * np.log(1 - h + delta)
        return (-1 / size) * (np.sum(costs, axis=0))

    def learn(self, lr, epoch):
        costs = []
        size = self._x_train.shape[0]
        jlen = self._y_train.shape[1]
        for i in range(epoch):
            # 10개의 숫자별로 계산
            for j in range(jlen):
                dt = (self.sigmoid(self._x_train, self.bias[:, j]) - self._y_train[:, j]).reshape(size,
                                                                                                  1) * self._x_train
                # 그래디언트 백터 계산
                self.bias[:, j] = self.bias[:, j] - lr * np.sum(dt, axis=0)

            cost = self.cost(self._x_train, self._y_train, self.bias)
            print(i, 'epoch, cost: ', cost)
            costs.append(cost)
        return self.bias, costs

    def predict(self, x, bias):
        size = self.bias.shape
        size = int(size[0])
        prediction = self.sigmoid(x.reshape(1, size), bias)
        return np.argmax(prediction)


# 학습
log = LogisticRegression(x_train, y_train, x_test, y_test)
bias, costs = log.learn(0.00000005, 500)
pre_cnt = 0
pre_wr =0
for i in range(0, 376):
    prediction = log.predict(x_test[i], bias)
    s1 = int(prediction/4)
    s2 = prediction%4
    reals1 = y_copy[i][0]
    reals2 = y_copy[i][1]
    if s1>s2 and reals1>reals2:
        pre_wr +=1
    elif s1==s2 and reals1==reals2:
        pre_wr +=1
    elif s1<s2 and reals1<reals2:
        pre_wr +=1
    print(i, ' predict: [',s1,' : ',s2,']', ' real: [',reals1,':',reals2,']')
    if s1 == reals1 and s2 == reals2:
        pre_cnt+=1
print("accuracy = ",pre_cnt/376)
print("winrate accuracy = ",pre_wr/376)