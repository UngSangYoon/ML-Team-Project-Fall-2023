import numpy as np
import json
from embed_and_norm import *
from util_func import *
from matplotlib import pyplot as plt

def load_datasets():
    seasons = ['03_04', '04_05', '05_06', '06_07', '07_08', '08_09', '09_10', '10_11', '11_12', '12_13', '13_14', '14_15', '15_16', '16_17', '17_18',
               '18_19', '19_20', '20_21', '21_22']
    new_seasons = ['17_18', '18_19', '19_20', '20_21', '21_22']
    stats = []
    scores = []
    for season in new_seasons:
        with open(f'new_dataset_add_team_stat/{season}.json', 'r') as f:
            stats_loaded = json.load(f)
        with open(f'new_dataset_add_team_stat/{season}_score.json', 'r') as f:
            scores_loaded = json.load(f)
        stats.extend(stats_loaded)
        scores.extend(scores_loaded)
    scores = np.array(scores, int)
    stats = np.array(stats)
    return stats, scores

stats, scores = load_datasets()

stats, min_vals, max_vals = normalize_stats(stats)
scores = normalize_scores(scores) # normalize scores to 0 ~ 1, where 0 means 0 and 1 means 4

# split datasets
(x_train, y_train), (x_test, y_test), (x_eval, y_eval) = train_test_eval_split(stats, scores, test_ratio=0.1, eval_ratio=0.1)
y_train = score_to_target(y_train)
y_copy = y_test
y_test = score_to_target(y_test)
y_eval = score_to_target(y_eval)
class LogisticRegression:
    def __init__(self, x_train, y_train, x_test, y_test, x_eval, y_eval):
        self._x_train = x_train
        self._y_train = y_train
        self._x_test = x_test
        self._y_test = y_test
        self._x_eval = x_eval
        self._y_eval = y_eval
        size_x = self._x_train.shape
        size_x = int(size_x[1])
        size_y = self._y_train.shape
        size_y = int(size_y[1])
        self.weights = random_init(size_x, size_y)

    def sigmoid(self, x, weights):
        return 1.0 / (1.0 + np.exp(-np.dot(x, weights)))

    def cost(self, x, y, weights):
        size = x.shape
        size = int(size[0])
        delta = 1e-10  # 무한대 방지
        h = self.sigmoid(x, weights)
        costs = y * np.log(h + delta) + (1 - y) * np.log(1 - h + delta)
        return (-1 / size) * (np.sum(costs, axis=0))

    def learn(self, lr, step, batch_size):
        costs = []
        eval_costs=[]
        size = self._x_train.shape[0]
        jlen = self._y_train.shape[1]
        for i in range(step):
            batch_mask = np.random.choice(size, batch_size)
            x_batch = self._x_train[batch_mask]
            y_batch = self._y_train[batch_mask]
            for j in range(jlen):
                dt = (self.sigmoid(x_batch, self.weights[:, j]) - y_batch[:, j]).reshape(batch_size,1) * x_batch
                # 그래디언트 백터 계산
                self.weights[:, j] = self.weights[:, j] - lr * np.sum(dt, axis=0)

            cost = sum(self.cost(x_batch, y_batch, self.weights))
            eval_cost = sum(self.cost(self._x_eval,self._y_eval,self.weights))
            if i % 100 == 0:
                print('step: ', i, 'cost: ', cost, 'eval_cost: ', eval_cost)
            costs.append(cost)
            eval_costs.append(eval_cost)
        return self.weights, costs, eval_costs

    def predict(self, x, weights):
        size = self.weights.shape
        size = int(size[0])
        prediction = self.sigmoid(x.reshape(1, size), weights)
        return np.argmax(prediction)

# 학습
log = LogisticRegression(x_train, y_train, x_test, y_test,x_eval,y_eval)
weights, costs, eval_costs = log.learn(0.000001, 10000, 200)
pre_cnt = 0
pre_wr = 0
for i in range (len(x_test)):
    prediction = log.predict(x_test[i], weights)
    s1 = int(prediction/5)
    s2 = prediction%5
    reals1 = y_copy[i][0]*4
    reals2 = y_copy[i][1]*4
    if s1>s2 and reals1>reals2:
        pre_wr +=1
    elif s1==s2 and reals1==reals2:
        pre_wr +=1
    elif s1<s2 and reals1<reals2:
        pre_wr +=1
    print(i, ' predict: [',s1,' : ',s2,']', ' real: [',reals1,':',reals2,']')
    if s1 == reals1 and s2 == reals2:
        pre_cnt+=1

print("accuracy = ",pre_cnt/i)
print("winrate accuracy = ",pre_wr/i)
plt.plot(costs,label='loss')
plt.savefig("Logistic_costs.png")
plt.show()
plt.cla()
plt.plot(eval_costs,label='eval loss')
plt.savefig("Logistic_evalloss.png")
plt.show()