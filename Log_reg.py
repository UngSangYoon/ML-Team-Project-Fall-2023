import numpy as np
import pandas as pd
df_wine = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data',header=None)
from sklearn.model_selection import train_test_split
x, y = df_wine.iloc[:, 1:].values, df_wine.iloc[:, 0].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=0)


def one_hot_encode_multiclass(y_change, num_classes=None):
    if num_classes is None:
        num_classes = np.max(y_change) + 1

    one_hot_labels = np.eye(num_classes)[y_change]

    return one_hot_labels
y_train = one_hot_encode_multiclass(y_train)
y_test = one_hot_encode_multiclass(y_test)
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
        delta = 1e-6  # 무한대 방지
        h = self.sigmoid(x, bias)
        costs = y * np.log(h + delta) + (1 - y) * np.log(1 - h + delta)
        return (-1 / size) * (np.sum(costs, axis=0))  # 각 행의 합 계산후 평균값을 구해 cost계산
    def learn(self, lr, epoch):
        costs=[]
        size = self._x_train.shape
        size = int(size[0])
        for i in range(epoch):
            # 10개의 숫자별로 계산
            for j in range(4):
                dt = (self.sigmoid(self._x_train, self.bias[:, j]) - self._y_train[:, j]).reshape(size,1)* self._x_train
                # 그래디언트 백터 계산
                self.bias[:, j] = self.bias[:, j] - lr * np.sum(dt, axis=0)
                # Learning Rate를 곱한 후 bias에 적용
            cost = self.cost(self._x_train, self._y_train, self.bias)
            print(i, 'epoch, cost: ',cost)
            costs.append(cost)
        return self.bias,costs
    def predict(self, x, bias):
        size = self.bias.shape
        size = int(size[0])
        prediction = self.sigmoid(x.reshape(1, size), bias)
        return np.argmax(prediction)

#학습
log = LogisticRegression(x_train, y_train, x_test, y_test)
bias, costs = log.learn(0.000001, 1500)
#정확도 예측 초기화
acc = 0
suc_rate=[0 for i in range(4)]
app_count=[0 for i in range(4)]
#실제 정확도 계산/출력
x, y = df_wine.iloc[:, 1:].values, df_wine.iloc[:, 0].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=0)
for i in range(0, 54):
    print(i, ' predict: ', log.predict(x_test[i], bias), ' real: ', y_test[i])
    app_count[y_test[i]]+=1
    if log.predict(x_test[i], bias) == y_test[i]:
        acc += 1.0
        suc_rate[y_test[i]]+=1
for i in range(4):
    if app_count[i] != 0:
        print(i, 'accuracy',suc_rate[i],'/',app_count[i]," ",suc_rate[i]/app_count[i])
print('accuracy: ', acc / 54.0)

