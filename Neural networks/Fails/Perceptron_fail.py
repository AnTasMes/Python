from activation_fun import ActivationFun
import numpy as np


class Perceptron:
    def __init__(self, iNo: int, hNo: int, oNo: int) -> None:
        # setting a number of inputs, neurons, and outputs
        self.input_nodes = iNo
        self.hidden_nodes = hNo
        self.output_nodes = oNo

        # synaptic w for input and hidden layer
        self.synaptic_weights = []
        self.synaptic_weights.append(2 * np.random.random((iNo, hNo)) - 1)
        self.synaptic_weights.append(2 * np.random.random((hNo, oNo)) - 1)

        # generic bias 1 1
        self.bias_m = np.array([1, 1])

        # learning rate
        self.lr = 0.1

    def think(self, inputs, level):
        # for i in range(layers) : we only have two possible layers here
        inputs += self.bias_m[level]
        inputs = ActivationFun.sigmoid(
            np.dot(inputs, self.synaptic_weights[level]))

        return inputs

    def train(self, training_inputs, traning_outputs):
        inputs = training_inputs
        # output = [] ==> [0] : input ; [1] : hidden
        output = []
        for i in range(2):
            output.append(self.think(inputs, i))

        # calculating Error and Hidden error
        error = training_outputs - output[1]
        hidden_error = np.dot(self.synaptic_weights[1], error.T)

        # calculating hidden -> output gradient
        gradient = ActivationFun.sigmoidDer(output[1]) * error * self.lr
        ho_delta = np.dot(gradient, output[0])
        self.synaptic_weights[1] += ho_delta.T
        self.bias_m[1] += gradient

        # calculating input -> hidden gradient
        gradient = ActivationFun.sigmoidDer(output[0]) * hidden_error * self.lr
        ih_delta = np.dot(gradient, inputs.T)
        self.synaptic_weights[0] += ih_delta
        self.bias_m[0] += gradient


if __name__ == "__main__":
    # in1 = 1 ; in2 = 0 ; bias = 1
    training_inputs = np.array([[1, 0], [1, 1], [0, 1], [0, 0]])
    training_outputs = np.array([[1, 0, 1, 0]])
    # print(f"TRAININ IN: \n{training_inputs}")
    p = Perceptron(2, 2, 1)
    for i in range(10000):
        output = p.train(training_inputs, training_outputs)

    # print(f"OUTPUTS: \n{output}")
    # y = p.think(training_inputs)
    # print(f"OUTPUT: \n{y}")
