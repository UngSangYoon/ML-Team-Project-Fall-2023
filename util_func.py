import numpy as np

# sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# softmax function
def softmax(x):
    c = np.max(x)
    exp_x = np.exp(x - c)
    return exp_x / np.sum(exp_x)

# batched cross entropy error
def cross_entropy_error(y, t):
    delta = 1e-7
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
             
    batch_size = y.shape[0]
    return -np.sum(np.log(y[np.arange(batch_size), t] + delta)) / batch_size

# random initialization
def random_init(n_in, n_out):
    return np.random.randn(n_in, n_out) * 0.01

# Xaiver initialization
def xaiver_init(n_in, n_out):
    return np.random.randn(n_in, n_out) / np.sqrt(n_in)

# He initialization
def he_init(n_in, n_out):
    return np.random.randn(n_in, n_out) * np.sqrt(2 / n_in)