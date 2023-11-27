import json
from util_func import *
from layers_nn import *
from embed_and_norm import *
from matplotlib import pyplot as plt


class ANN:
    def __init__(
        self, input_size, hidden_size, output_size, learning_rate, is_DNN_with_ADAM
    ):
        # important! is_DNN_with_ADAM: True if DNN and ADAM, False if shallow and SGD
        self.is_DNN_with_ADAM = is_DNN_with_ADAM

        # 가중치 초기화
        self.learning_rate = learning_rate
        params = {}
        params["W1"] = he_init(input_size, hidden_size)
        params["b1"] = np.zeros(hidden_size)
        params["W2"] = he_init(hidden_size, hidden_size)
        params["b2"] = np.zeros(hidden_size)
        params["W3"] = he_init(hidden_size, output_size)
        params["b3"] = np.zeros(output_size)

        if self.is_DNN_with_ADAM:
            # Build layers
            self.layers = [
                Affine(params["W1"], params["b1"]),
                BatchNorm(hidden_size),
                LeakyReLU(),
                Dropout(0.5),
                Affine(params["W2"], params["b2"]),
                BatchNorm(hidden_size),
                LeakyReLU(),
                Dropout(0.5),
                Affine(params["W3"], params["b3"]),
            ]
        else:
            self.layers = [
                Affine(params["W1"], params["b1"]),
                LeakyReLU(),
                Affine(params["W3"], params["b3"]),
            ]

        self.last_layer = MSELoss()

        self.loss_list = []
        self.eval_loss_list = []

    def forward(self, x, train):
        for layer in self.layers:
            if isinstance(layer, Dropout):
                x = layer.forward(x, train)
            else:
                x = layer.forward(x)
        return x

    def loss(self, input, target):
        output = self.forward(input, train=True)
        loss = self.last_layer.forward(output, target)
        return loss

    def backward(self, input, target):
        self.loss(input, target)
        dout = 1
        dout = self.last_layer.backward(dout)
        for layer in reversed(self.layers):
            dout = layer.backward(dout)
        return

    def update_params(self, lr_decay=1):
        for layer in self.layers:
            if isinstance(layer, Affine):
                layer.W -= self.learning_rate * layer.dW
                layer.b -= self.learning_rate * layer.db
            elif isinstance(layer, BatchNorm):
                layer.gamma -= self.learning_rate * layer.dgamma
                layer.beta -= self.learning_rate * layer.dbeta
        self.lr_decay(lr_decay)

    def update_params_adam(self, lr_decay=1):
        for layer in self.layers:
            if isinstance(layer, Affine):
                layer.t += 1
                layer.dW_m, layer.dW_v, layer.dW = adam(
                    layer.dW, layer.dW_m, layer.dW_v, layer.t
                )
                layer.db_m, layer.db_v, layer.db = adam(
                    layer.db, layer.db_m, layer.db_v, layer.t
                )
                layer.W -= self.learning_rate * layer.dW
                layer.b -= self.learning_rate * layer.db
            elif isinstance(layer, BatchNorm):
                layer.t += 1
                layer.dgamma_m, layer.dgamma_v, layer.dgamma = adam(
                    layer.dgamma, layer.dgamma_m, layer.dgamma_v, layer.t
                )
                layer.dbeta_m, layer.dbeta_v, layer.dbeta = adam(
                    layer.dbeta, layer.dbeta_m, layer.dbeta_v, layer.t
                )
                layer.gamma -= self.learning_rate * layer.dgamma
                layer.beta -= self.learning_rate * layer.dbeta
        self.lr_decay(lr_decay)

    def lr_decay(self, decay_rate):
        self.learning_rate *= decay_rate

    def learn(
        self,
        input,
        target,
        eval_input,
        eval_target,
        iters_num,
        batch_size,
        loss_interval,
        lr_decay,
    ):
        data_size = input.shape[0]
        for i in range(iters_num):
            batch_mask = np.random.choice(data_size, batch_size)
            input_batch = input[batch_mask]
            target_batch = target[batch_mask]
            self.backward(input_batch, target_batch)
            if self.is_DNN_with_ADAM:
                self.update_params_adam(lr_decay=lr_decay)
            else:
                self.update_params(lr_decay=lr_decay)
            if i % loss_interval == 0:
                loss = self.loss(input_batch, target_batch)
                eval_loss = self.loss(eval_input, eval_target)
                self.loss_list.append(loss)
                self.eval_loss_list.append(eval_loss)
                print(
                    f"iter {i}, loss: {loss}, eval loss: {eval_loss}, lr: {self.learning_rate}"
                )

    def predict(self, input):
        output = self.forward(input, train=False)
        output[output < 0] = 0
        return np.around(output * 4)

    def accuracy(self, input, target):
        output = self.predict(input)
        target = np.around(target * 4)

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
    seasons = [
        "03_04",
        "04_05",
        "05_06",
        "06_07",
        "07_08",
        "08_09",
        "09_10",
        "10_11",
        "11_12",
        "12_13",
        "13_14",
        "14_15",
        "15_16",
        "16_17",
        "17_18",
        "18_19",
        "19_20",
        "20_21",
        "21_22",
    ]
    new_seasons = ["17_18", "18_19", "19_20", "20_21", "21_22"]
    stats = []
    scores = []
    for season in new_seasons:
        with open(f"new_dataset/{season}.json", "r") as f:
            stats_loaded = json.load(f)
        with open(f"new_dataset/{season}_score.json", "r") as f:
            scores_loaded = json.load(f)
        stats.extend(stats_loaded)
        scores.extend(scores_loaded)
    scores = np.array(scores, int)
    stats = np.array(stats)
    return stats, scores


def run(
    input_size=306,
    hidden_size=306,
    output_size=2,
    learning_rate=0.002,
    is_DNN_with_ADAM=True,
):
    stats, scores = load_datasets()

    stats, min_vals, max_vals = normalize_stats(stats)
    scores = normalize_scores(
        scores
    )  # normalize scores to 0 ~ 1, where 0 means 0 and 1 means 4

    # split datasets
    (
        (train_stats, train_scores),
        (test_stats, test_scores),
        (eval_stats, eval_scores),
    ) = train_test_eval_split(stats, scores, test_ratio=0.1, eval_ratio=0.1)

    ann = ANN(
        input_size=input_size,
        hidden_size=hidden_size,
        output_size=output_size,
        learning_rate=learning_rate,
        is_DNN_with_ADAM=is_DNN_with_ADAM,
    )
    ann.learn(
        train_stats,
        train_scores,
        eval_stats,
        eval_scores,
        iters_num=10000,
        batch_size=200,
        loss_interval=100,
        lr_decay=0.99995,
    )

    predict_score = ann.predict(test_stats)[:10]
    real_score = np.around(test_scores[:10] * 4)
    for i in range(10):
        print(
            i,
            " predict: [",
            int(predict_score[i][0]),
            ":",
            int(predict_score[i][1]),
            "]",
            " real: [",
            int(real_score[i][0]),
            ":",
            int(real_score[i][1]),
            "]",
        )
    acc, acc_win = ann.accuracy(test_stats, test_scores)
    print(f"accuracy: {acc}, winning accuracy: {acc_win}")

    # show loss and eval loss
    plt.plot(ann.loss_list, label="loss")
    plt.plot(ann.eval_loss_list, label="eval loss")
    plt.legend()
    plt.show()
