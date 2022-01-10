import numpy as np


class ActivationFun:
    @staticmethod
    def step(x, thold=0.95):
        return [1 if elem >= thold else 0 for elem in x]

    @staticmethod
    def sigmoidDer(x):
        return x * (1 - x)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def cosHyperbolic(x):
        return (1 + np.exp(-2 * x)) / (2 * np.exp(-x))

    @staticmethod
    def tanHyperbolic(x):
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    @staticmethod
    def tanHyperbolicDer(x):
        return 1 - (
            np.power(np.exp(x) - np.exp(-x), 2) / np.power(np.exp(x) + np.exp(-x), 2)
        )


if __name__ == "__main__":
    print(f"Result for tanh(20) : {ActivationFun.tanHyperbolic(x = 20)}")
    print(f"Result for tanh(20)': {ActivationFun.tanHyperbolicDer(x = 20)}")
