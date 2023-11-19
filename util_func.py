import numpy as np

# sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# softmax function
def softmax(x):
    c = np.max(x)
    exp_x = np.exp(x - c)
    return exp_x / np.sum(exp_x)

# batched mean squared error
def mean_squared_error(y, t):
    return 0.5 * np.sum((y - t)**2) / y.shape[0]

# batched cross entropy error
def cross_entropy_error(y, t):
    delta = 1e-7
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)
             
    batch_size = y.shape[0]
    return -np.sum(t * np.log(y + delta)) / batch_size

# random initialization
def random_init(n_in, n_out):
    return np.random.randn(n_in, n_out) * 0.01

# Xavier initialization
def xavier_init(n_in, n_out):
    return np.random.randn(n_in, n_out) / np.sqrt(n_in)

# He initialization
def he_init(n_in, n_out):
    return np.random.randn(n_in, n_out) * np.sqrt(2 / n_in)

def train_test_eval_split(input_data, target_data, test_ratio, eval_ratio):
    data_size = input_data.shape[0]
    shuffle_mask = np.random.choice(data_size, data_size, replace=False)
    input_data = input_data[shuffle_mask]
    target_data = target_data[shuffle_mask]
    test_size = int(data_size * test_ratio)
    eval_size = int(data_size * eval_ratio)
    test_input = input_data[:test_size]
    test_target = target_data[:test_size]
    eval_input = input_data[test_size:test_size+eval_size]
    eval_target = target_data[test_size:test_size+eval_size]
    train_input = input_data[test_size+eval_size:]
    train_target = target_data[test_size+eval_size:]
    return (train_input, train_target), (test_input, test_target), (eval_input, eval_target)