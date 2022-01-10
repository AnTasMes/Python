from activation_fun import ActivationFun
import numpy as np


class Perceptron:
    def __init__(self, inputNo) -> None:
        self.synaptic_weights = 2 * np.random.random((inputNo, 1)) - 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def treshold(self, x, thold=0.7):
        return [1 if elem >= thold else 0 for elem in x]

    def sigmoidDerivative(self, x):
        return x * (1 - x)

    def think(self, input, simpleAF=False):
        input = input.astype(float)
        if simpleAF:
            return ActivationFun.step(
                self.sigmoid(np.dot(input, self.synaptic_weights))
            )
        else:
            return ActivationFun.sigmoid(np.dot(input, self.synaptic_weights))

    def train(self, training_input, training_output, iter=20000, simpleAF=False):
        for i in range(iter):
            output = self.think(training_input, simpleAF)
            error = training_output - output
            if simpleAF:
                adj = np.dot(training_input.T, error)
            else:
                adj = np.dot(training_input.T, error * ActivationFun.sigmoidDer(output))
            self.synaptic_weights += adj


if __name__ == "__main__":
    # training_inputs = np.array([[1, 1, 1], [1, 1, 0], [0, 1, 1], [0, 1, 0]])

    training_inputs = np.array([[1, 1, 0, 1], [1, 0, 0, 1], [1, 1, 0, 0], [1, 0, 1, 1]])
    training_ouputs = np.array([[1, 0, 1, 0]]).T

    p = Perceptron(training_inputs.size // len(training_inputs))
    p.train(training_inputs, training_ouputs)

    print(f"OUTPUT: {p.think(np.array([[1, 1, 1, 1]]))}")
