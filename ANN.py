import json
from util_func import *
from layers_nn import *
from embed_and_norm import *

class ANN:
    def __init__(self, input_size, hidden_size, output_size, learning_rate):
        # 가중치 초기화
        self.learning_rate = learning_rate
        params = {}
        params["W1"] = xavier_init(input_size, hidden_size)
        params["b1"] = np.zeros(hidden_size)
        params["W2"] = xavier_init(hidden_size, output_size)
        params["b2"] = np.zeros(output_size)

        # Build layers
        self.layers = [
            Affine(params["W1"], params["b1"]),
            ReLU(),
            Affine(params["W2"], params["b2"]),
        ]

        self.last_layer = SoftmaxWithLoss()

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
    
    def learn(self, input, target, iters_num, batch_size):
        data_size = input.shape[0]
        for i in range(iters_num):
            batch_mask = np.random.choice(data_size, batch_size)
            input_batch = input[batch_mask]
            target_batch = target[batch_mask]
            self.backward(input_batch, target_batch)
            self.update_params()
            if i % 10 == 0:
                print(f"iter {i}, loss: {self.loss(input, target)}")

    def predict(self, input):
        output = self.forward(input)
        return target_to_score(output)

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

ann = ANN(input_size=156, hidden_size=156, output_size=25, learning_rate=0.0001)
ann.learn(stats, score_to_target(scores), iters_num=5000, batch_size=1000)