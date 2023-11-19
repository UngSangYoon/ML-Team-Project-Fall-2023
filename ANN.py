import json
from util_func import *
from layers_nn import *
from embed_and_norm import *

class ANN:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        # 가중치 초기화
        self.learning_rate = learning_rate
        params = {}
        params["W1"] = he_init(input_size, hidden_size*4)
        params["b1"] = np.zeros(hidden_size*4)
        params["W2"] = he_init(hidden_size*4, hidden_size)
        params["b2"] = np.zeros(hidden_size)
        params["W3"] = he_init(hidden_size, hidden_size//2)
        params["b3"] = np.zeros(hidden_size//2)
        params["W4"] = he_init(hidden_size//2, output_size)
        params["b4"] = np.zeros(output_size)

        # Build layers
        self.layers = [
            Affine(params["W1"], params["b1"]),
            BatchNorm(),
            ReLU(),
            Affine(params["W2"], params["b2"]),
            BatchNorm(),
            ReLU(),
            Affine(params["W3"], params["b3"]),
            BatchNorm(),
            ReLU(),
            Affine(params["W4"], params["b4"]),
        ]

        self.last_layer = MSELoss()

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def loss(self, input, target):
        output = self.forward(input)
        loss = self.last_layer.forward(output, target)
        return loss

    def backward(self, input, target):
        self.loss(input, target)
        dout = 1
        dout = self.last_layer.backward(dout)
        for layer in reversed(self.layers):
            dout = layer.backward(dout)
        return

    def update_params(self):
        for layer in self.layers:
            if isinstance(layer, Affine):
                layer.W -= self.learning_rate * layer.dW
                layer.b -= self.learning_rate * layer.db
    
    def learn(self, input, target, eval_input, eval_target, iters_num, batch_size, loss_interval):
        data_size = input.shape[0]
        for i in range(iters_num):
            batch_mask = np.random.choice(data_size, batch_size)
            input_batch = input[batch_mask]
            target_batch = target[batch_mask]
            self.backward(input_batch, target_batch)
            self.update_params()
            if i % loss_interval == 0:
                print(f"iter {i}, loss: {self.loss(input_batch, target_batch)}, eval loss: {self.loss(eval_input, eval_target)}")

    def predict(self, input):
        output = self.forward(input)
        output[output < 0] = 0
        return np.around(output*4)

    def accuracy(self, input, target):
        output = self.predict(input)
        target = np.around(target*4)

        # accuracy
        correct = 0
        for i in range(len(output)):
            if output[i][0] == target[i][0] and output[i][1] == target[i][1]:
                correct += 1
        acc = correct / len(output)

        # winning accuracy
        correct = 0
        for i in range(len(output)):
            if output[i][0] > output[i][1] and target[i][0] > target[i][1]:
                correct += 1
            elif output[i][0] < output[i][1] and target[i][0] < target[i][1]:
                correct += 1
            elif output[i][0] == output[i][1] and target[i][0] == target[i][1]:
                correct += 1
        win_acc = correct / len(output)

        return acc, win_acc

def load_datasets():
    seasons = ['03_04', '04_05', '05_06', '06_07', '07_08']
    stats = []
    scores = []
    for season in seasons:
        with open(f'dataset/{season}.json', 'r') as f:
            stats_loaded = json.load(f)
        with open(f'dataset/{season}_score.json', 'r') as f:
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
(train_stats, train_scores), (test_stats, test_scores), (eval_stats, eval_scores) = train_test_eval_split(stats, scores, test_ratio=0.1, eval_ratio=0.1)

ann = ANN(input_size=156, hidden_size=156, output_size=2, learning_rate=0.001)
ann.learn(train_stats, train_scores, eval_stats, eval_scores, iters_num=10000, batch_size=100, loss_interval=100)
ann.predict(test_stats)[:10]
np.around(test_scores[:10]*4)
acc, acc_win = ann.accuracy(test_stats, test_scores)
print(f"accuracy: {acc}, winning accuracy: {acc_win}")