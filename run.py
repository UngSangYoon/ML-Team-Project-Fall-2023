import Log_reg
import ANN

if __name__ == "__main__":
    print('Logistic Regression')
    Log_reg.run()
    print()
    print('Shallow Neural Network with SGD')
    ANN.run(input_size=306, hidden_size=306//6, output_size=2, learning_rate=0.002, is_DNN_with_ADAM=False)
    print()
    print('Deep Neural Network with ADAM')
    ANN.run(input_size=306, hidden_size=306//6, output_size=2, learning_rate=0.002, is_DNN_with_ADAM=True)