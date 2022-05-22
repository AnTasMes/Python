from abc import abstractclassmethod
import numpy as np


class Activation():
    _repository = {}

    def __init_subclass__(cls, prefix, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._repository[prefix] = cls

    def __new__(cls, **kwargs):
        cls = cls._repository[kwargs['prefix']]

        obj = object.__new__(cls)
        return obj

    @abstractclassmethod
    def function(self, x):
        pass

    @abstractclassmethod
    def derivative(self, x):
        pass


class Sigmoid(Activation, prefix='sigmoid'):
    def function(self, x):
        return 1 / (1 + np.exp(-x))

    def derivative(self, x):
        return x * (1 - x)


class Hyperbolic(Activation, prefix='htan'):
    def function(self, x):
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    def derivative(self, x):
        return 1 - (
            np.power(np.exp(x) - np.exp(-x), 2) /
            np.power(np.exp(x) + np.exp(-x), 2)
        )


class ReLU(Activation, prefix='relu'):
    def function(self, x):
        x[x <= 0] = 0
        x[x > 0] = x[x > 0]
        return x

    def derivative(self, x):
        return 1 * (x > 0)