from activation_fun import ActivationFun as af
import flex_a_fun as faf

import numpy as np


class Perceptron:
    def __init__(self, input_nodes: int, hidden_layers: list, output_nodes: int, fun: dict = None) -> None:
        """
        Init for a multilayer perceptron

        Parameters
        ----------
        :param int input_nodes: 
            Number of input `nodes`
        :param list of int hidden_layers: 
            A list of numbers of neurons per each `hidden layer`
        :param int output_nodes:
            Number of output `nodes`

        Examples
        --------
        >>> p = Perceptron(2, [3,3], 2)
        >>> print(p.Synaptic_Weights[0])
        [[ 0.57519168  0.29013704]
        [-0.0346663  -0.26533394]
        [-0.43970131 -0.41541983]]
        >>> print(p.Synaptic_Weights[1])
        [[ 0.83238601  0.27162139 -0.06089101]
        [ 0.96001736  0.90498205 -0.1313054 ]
        [-0.48583136 -0.68419176 -0.86352844]]
        >>> print(p.Synaptic_Weights[2])
        [[ 0.51967537 -0.59031319 -0.2042105 ]]

        Where the values of weights are calculated by ``2 * np.random.random([O_nodes, IN_nodes]) - 1``
        """

        # adding a list of wanted functions
        self.Funcions = fun

        self.Input_Nodes = input_nodes
        self.Output_Nodes = output_nodes
        self.Hidden_Layers = hidden_layers

        self.Learning_Rate = 0.1

        self.Synaptic_Weights = []
        self.Bias = []

        # Putting all layers into one list
        self.Layers = [input_nodes]
        for i in hidden_layers:
            self.Layers.append(i)
        self.Layers.append(output_nodes)

        for i in range(len(self.Layers)-1):
            # adding synaptic weights
            self.Synaptic_Weights.append(
                2 * np.random.random([self.Layers[i+1], self.Layers[i]]) - 1)
            # adding bias
            self.Bias.append(2 * np.random.random([self.Layers[i+1], 1]) - 1)

        # finally adding functions to the network
        self.AddFunctions()

    def AddFunctions(self):
        self.f_list = ['sigmoid' for i in self.Synaptic_Weights]

        # adds wanted functions to the list for later use
        if self.Funcions:
            for key, elem in self.Funcions.items():
                self.f_list[int(key)] = elem

    def FeedForward(self, inputs: np.ndarray):
        """
        A method for calculating the result of an input

        Parameters
        ----------
        :param np.ndarray inputs:
            array of inputs for calculation. This array should be send `transposed`

        Return
        ------
        list of int
            List of outputs for each layer of the network. Last element is the final output

        Examples
        --------
        >>> training_inputs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
        >>> p.FeedForward(np.array([training_inputs[3]]).T)
        [[0.9788282]]
        """
        Outputs = []

        for i in range(len(self.Synaptic_Weights)):
            inputs = af.sigmoid(
                np.dot(self.Synaptic_Weights[i], inputs) + self.Bias[i])

            Outputs.append(inputs)

        return Outputs

    def FeedForwardFlex(self, inputs: np.ndarray):
        Outputs = []

        for i in range(len(self.Synaptic_Weights)):
            inputs = faf.Activation(prefix=self.f_list[i]).function(
                np.dot(self.Synaptic_Weights[i], inputs) + self.Bias[i])

            Outputs.append(inputs)

        return Outputs

    def BackPropagation(self, guesses: list, outputs: np.ndarray, ins: np.ndarray):
        errors = []

        errors.append(outputs - guesses[-1])

        for i in range(len(guesses)-1, -1, -1):
            # calculating gradient
            grad = af.sigmoidDer(guesses[i]) * errors[-1] * self.Learning_Rate

            # adding to bias
            self.Bias[i] += grad

            # adding to synaptic weights
            if i > 0:
                self.Synaptic_Weights[i] += np.dot(grad, guesses[i-1].T)
            else:
                # if at last layer use Inputs for gradient
                self.Synaptic_Weights[i] += np.dot(grad, ins.T)

            # adding new error (always using the last error) (this doesn't have to be a list)
            errors.append(np.dot(self.Synaptic_Weights[i].T, errors[-1]))

    def BackPropagationFlex(self, guesses: list, outputs: np.ndarray, ins: np.ndarray):
        errors = []

        errors.append(outputs - guesses[-1])

        for i in range(len(guesses)-1, -1, -1):
            # calculating gradient
            grad = faf.Activation(prefix=self.f_list[i]).derivative(
                guesses[i]) * errors[-1] * self.Learning_Rate

            # adding to bias
            self.Bias[i] += grad

            # adding to synaptic weights
            if i > 0:
                self.Synaptic_Weights[i] += np.dot(grad, guesses[i-1].T)
            else:
                # if at last layer use Inputs for gradient
                self.Synaptic_Weights[i] += np.dot(grad, ins.T)

            # adding new error (always using the last error) (this doesn't have to be a list)
            errors.append(np.dot(self.Synaptic_Weights[i].T, errors[-1]))

    def Train(self, inputs: np.ndarray, outputs: np.ndarray, iter: int):
        """
        Method for training the network for `iter` amount of cycles 

        This method is used by the user to train its network. Matching
        the number of parameters for each layer is important.

        Parameters
        ----------
        :param np.ndarray inputs:
            Array of input data
        :param np.ndarray outputs:
            Array of outputs to be tested
        :param int iter:
            Number of itterations

        Examples
        --------
        >>> training_inputs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
        >>> training_ouputs = np.array([[0], [0], [1], [1]])
        >>> p.Train(training_inputs, training_ouputs, 20000)
        """
        for i in range(iter):
            index = np.random.randint(0, len(inputs))

            # makes parameter data transposed
            t_inputs = np.array([inputs[index]]).T
            t_outputs = np.array([outputs[index]]).T

            guesses = self.FeedForwardFlex(t_inputs)
            self.BackPropagationFlex(guesses, t_outputs, t_inputs)


if __name__ == "__main__":
    activation_dict = {
        '0': 'htan',
        '1': 'htan',
        '2': 'htan'
    }

    p = Perceptron(2, [3, 3], 1)

    training_inputs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
    training_ouputs = np.array([[0], [0], [1], [1]])

    #v = p.FeedForwardFlex(np.array([training_inputs[3]]).T)

    # print(type(training_inputs))
    p.Train(training_inputs, training_ouputs, 20000)

    o = p.FeedForward(np.array([training_inputs[3]]).T)
    print(o[-1])
