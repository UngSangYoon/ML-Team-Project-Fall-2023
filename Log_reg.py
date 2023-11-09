import numpy as np
from dataset.mnist import load_mnist

(x_train, y_train), (x_test, y_test) = load_mnist(flatten=True, normalize=True, one_hot_label=True)

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
        for i in range(epoch):
            # 10개의 숫자별로 계산
            for j in range(10):
                dt = (self.sigmoid(self._x_train, self.bias[:, j]) - self._y_train[:, j])
                dt = dt.reshape(-1, 1)
                dt=dt*self._x_train
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
log = LogisticRegression(x_train, y_train, x_test, y_test)
bias, costs = log.learn(0.000001, 50)
acc = 0
suc_rate=[0 for i in range(10)]
app_count=[0 for i in range(10)]
(x_train, y_train), (x_test, y_test) = load_mnist(flatten=True, normalize=True)
for i in range(0, 1000):
    print(i, ' predict: ', log.predict(x_test[i], bias), ' real: ', y_test[i])
    app_count[y_test[i]]+=1
    if log.predict(x_test[i], bias) == y_test[i]:
        acc += 1.0
        suc_rate[y_test[i]]+=1
for i in range(10):
    print(i, 'accuracy',suc_rate[i],'/',app_count[i]," ",suc_rate[i]/app_count[i])
print('accuracy: ', acc / 1000.0)

