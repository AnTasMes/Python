from ast import Del
from activation_fun import ActivationFun
import numpy as np


class Perceptron:
    def __init__(self, input_nodes, hidden_nodes, output_nodes) -> None:
        self.Input_Nodes = input_nodes
        self.Hidden_Nodes = hidden_nodes
        self.Output_Nodes = output_nodes

        self.Synaptic_Weights_IH = 2 * \
            np.random.random((hidden_nodes, input_nodes)) - 1
        self.Synaptic_Weights_HO = 2 * \
            np.random.random((output_nodes, hidden_nodes)) - 1

        self.Bias_h = 2 * np.random.random((hidden_nodes, 1)) - 1
        self.Bias_o = 2 * np.random.random((output_nodes, 1)) - 1

        self.Learning_rate = 0.1

        self.Synaptic_Weights_TST = np.array([[1, 2], [2, 1]])
        self.Synaptic_Weights_TST2 = np.array([[1, 2]])

        self.CurrError = 1
        self.EpsCounter = 5

    def PrintPerceptron(self):
        print(f"SW_IH: \n{self.Synaptic_Weights_IH}\n")
        print(f"SW_HO: \n{self.Synaptic_Weights_HO}\n")
        print(f"Bias_H: \n{self.Bias_h}\n")
        print(f"Bias_O: \n{self.Bias_o}\n")

    def PrintInputsOutputs(self, t_inputs, t_outputs):
        print(f"T_Inputs: \n{t_inputs}\n")
        print(f"T_Inputs_T: \n{t_inputs.T}\n")
        print(f"T_Outputs: \n{t_outputs}\n")
        print(f"T_Outputs_T: \n{t_outputs.T}\n")

    def FeedForward(self, inputs):
        # calculating hidden layer
        HiddenOutputs = ActivationFun.sigmoid(
            np.dot(self.Synaptic_Weights_IH, inputs) + self.Bias_h)

        # calculating output layer (guess layer)
        GuessOutputs = ActivationFun.sigmoid(
            np.dot(self.Synaptic_Weights_HO, HiddenOutputs) + self.Bias_o)

        return HiddenOutputs, GuessOutputs

    def Train(self, t_inputs, t_outputs):

        HiddenOutputs, GuessOutputs = self.FeedForward(t_inputs)

        # calculating output error
        ErrorsOutput = t_outputs - GuessOutputs

        # calculating output gradient based on error
        GradientsOutput = ActivationFun.sigmoidDer(
            GuessOutputs) * ErrorsOutput * self.Learning_rate

        # adding to bias
        self.Bias_o += GradientsOutput

        # changing synapic weights
        DeltaWHO = np.dot(GradientsOutput, HiddenOutputs.T)
        self.Synaptic_Weights_HO += DeltaWHO

        ErrorsHidden = np.dot(self.Synaptic_Weights_HO.T, ErrorsOutput)
        GradientsHidden = ActivationFun.sigmoidDer(
            HiddenOutputs) * ErrorsHidden * self.Learning_rate

        self.Bias_h += GradientsHidden

        DeltaWIH = np.dot(GradientsHidden, t_inputs.T)
        self.Synaptic_Weights_IH += DeltaWIH


if __name__ == "__main__":
    p = Perceptron(2, 3, 1)

    training_inputs = np.array([[1, 1], [0, 0], [1, 0], [0, 1]])
    training_ouputs = np.array([[0], [0], [1], [1]])

    #training_input_2 = np.array([[2, 6]]).T

    p.PrintPerceptron()
    p.PrintInputsOutputs(training_inputs[0], training_ouputs[0])

    # p.FeedForward(training_inputs[0].T)

    # p.Train(np.array([training_inputs[0]]).T,
    #         np.array([training_ouputs[0]]).T)

    for i in range(20000):
        index = np.random.randint(0, 4)
        stop = p.Train(np.array([training_inputs[index]]).T,
                       np.array([training_ouputs[index]]).T)
        if stop == 0:
            break

    Hidden, Guess = p.FeedForward(np.array([training_inputs[0]]).T)
    print(F"1,1: {Guess}")

    Hidden, Guess = p.FeedForward(np.array([training_inputs[1]]).T)
    print(F"0,0: {Guess}")

    Hidden, Guess = p.FeedForward(np.array([training_inputs[2]]).T)
    print(F"1,0: {Guess}")

    Hidden, Guess = p.FeedForward(np.array([training_inputs[3]]).T)
    print(F"0,1: {Guess}")

    # p.FeedForward(training_inputs[0])
    # for i in range(1):
    #     index = np.random.randint(0, 4)
    #     p.Train(training_inputs[index], training_ouputs[index])

    # HiddenOutputs = np.array([HiddenOutputs])
    # GuessOutputs = np.array([GuessOutputs])

    # print(f"H_OUTPUTS: \n{HiddenOutputs}\n")
    # print(f"G_OUTPUTS: \n{GuessOutputs}\n")
