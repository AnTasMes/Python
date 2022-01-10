import numpy as np


class NeuralNetwork:
    def __init__(
        self,
    ) -> None:
        np.random.seed(1)
        self.synaptic_weights = 2 * np.random.random((3, 1)) - 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoidDerivative(self, x):
        return x * (1 - x)

    def train(self, training_inputs, training_outputs, training_iter):
        for iter in range(training_iter):
            output = self.think(training_inputs)
            error = training_outputs - output
            adj = np.dot(training_inputs.T, error * self.sigmoidDerivative(output))
            self.synaptic_weights += adj

    def think(self, inputs):
        inputs = inputs.astype(float)
        outputs = self.sigmoid(np.dot(inputs, self.synaptic_weights))
        return outputs


if __name__ == "__main__":
    neural_network = NeuralNetwork()

    print(f"Neural synaptic weights: \n{neural_network.synaptic_weights}")

    training_inputs = np.array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])

    training_outputs = np.array([[0, 1, 1, 0]]).T

    neural_network.train(training_inputs, training_outputs, 20000)

    print(
        f"Neural synaptic weights (after training): \n{neural_network.synaptic_weights}"
    )

    print(f"Output for [1,1,1]: \n{neural_network.think(np.array([1,1,1]))}")
