import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def ErrorWeightetDerivative(x):
    return x*(1-x)

training_input = np.array([[0,0,1],
                            [1,1,1],
                            [1,0,1],
                            [0,1,1]])

training_output = np.array([[0,1,1,0]]).T 

np.random.seed(1)

synaptic_weights = 2*np.random.random((3,1)) - 1

print(f'Random weights\n{synaptic_weights}')

for it in range(20000):
    input_layer = training_input
    output_layer = sigmoid(np.dot(input_layer, synaptic_weights))
    error = training_output - output_layer 
    adj = error * ErrorWeightetDerivative(output_layer)

    synaptic_weights += np.dot(input_layer.T, adj)

print(f'Random weights after training:\n{synaptic_weights}')

print(f'Output after training: \n{output_layer}')