import json
from util_func import *
from layers_nn import *


class ANN:
    def __init__(self, input, target, input_size, hidden_size, output_size, epoch, learning_rate):
        # 가중치 초기화
        self.input = input
        self.target = target
        self.epoch = epoch
        self.learning_rate = learning_rate
        self.params = {}
        self.params["W1"] = xaiver_init(input_size, hidden_size)
        self.params["b1"] = np.zeros(hidden_size)
        self.params["W2"] = xaiver_init(hidden_size, output_size)
        self.params["b2"] = np.zeros(output_size)

        # Build layers
        self.layers = [
            Affine(self.params["W1"], self.params["b1"]),
            ReLU(),
            Affine(self.params["W2"], self.params["b2"]),
        ]

    def forward(self):
        self.input = input
        for layer in self.layers:
            input = layer.forward(input)
        return input

    def loss(self):
        output = self.forward(input)
        loss = SoftmaxWithLoss.forward(output, target)
        return loss

    def backward(self):
        dout = 1
        dout = self.last_layer.backward(dout)
        for layer in reversed(self.layers):
            dout = layer.backward(dout)

    def update_params(self):
        for layer in self.layers:
            if isinstance(layer, Affine):
                layer.W -= self.learning_rate * layer.dW
                layer.b -= self.learning_rate * layer.db
    
    def learn(self):
