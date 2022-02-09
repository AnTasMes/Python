from email.parser import FeedParser
from mimetypes import guess_extension
from xml.dom.pulldom import END_ELEMENT
from activation_fun import ActivationFun
import numpy as np

# programming a two layer perceptron (input layer, hidden layer, output layer)
# Perceptron(input_nodes, hidden_nodes, output_nodes) => p = Perceptron(2,3,1)
# Preparation for multi_hidden_layer perceptron with looping


class Perceptron:
    def __init__(self, input_nodes: int, hidden_nodes: int, output_nodes: int) -> None:
        self.Input_Nodes = input_nodes
        self.Output_Nodes = output_nodes
        self.Hidden_Nodes = hidden_nodes

        self.Learning_Rate = 0.1

        self.Synaptic_Weights = []
        self.Bias = []

        # representing layers through a list of numbers
        self.Layers = [input_nodes, hidden_nodes, output_nodes]

        for i in range(len(self.Layers)-1):
            # setting up synaptic weights
            self.Synaptic_Weights.append(
                2 * np.random.random([self.Layers[i+1], self.Layers[i]]) - 1)
            # adding bias
            self.Bias.append(
                2 * np.random.random([self.Layers[i+1], 1]) - 1)

    def FeedForward(self, inputs):
        Outputs = []
        Outputs.append(inputs)
        for i in range(len(self.Layers)-1):
            # calculating hidden and guess outputs
            Outputs.append(ActivationFun.sigmoid(
                (np.dot(self.Synaptic_Weights[i], inputs))+self.Bias[i]))
            inputs = Outputs[i]

        return Outputs

    def Backpropagate(self, t_inputs, t_ouputs):
        Outputs = self.FeedForward(t_inputs)
        Gradients = []

        Error = t_ouputs - Outputs[-1]

        # 2 Gradienta
        # 2 Bias update
        # 2 Delta update
        # 2 SW update

        Gradient = ActivationFun.sigmoidDer(
            Outputs[2]) * Error * self.Learning_Rate
        self.Bias[1] += Gradient
        Delta = np.dot(Gradient, Outputs[1].T)
        self.Synaptic_Weights[1] += Delta

        Error = np.dot(self.Synaptic_Weights[1].T, Error)
        Gradient = ActivationFun.sigmoidDer(
            Outputs[1]) * Error * self.Learning_Rate
        self.Bias[0] += Gradient
        Delta = np.dot(Gradient, Outputs[0].T)


if __name__ == "__main__":
    p = Perceptron(2, 2, 1)

    training_inputs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
    training_outputs = np.array([[0], [0], [1], [1]])

    # p.FeedForward(np.array([training_inputs[0]]).T)

    p.Backpropagate(np.array([training_inputs[0]]).T,
                    np.array([training_outputs[0]]).T)

    # print(f"SW:\n{self.Synaptic_Weights[i]}\n")
    #         print(f"BIAS:\n{self.Bias[i]}\n")
