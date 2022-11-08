import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-1 * x))


class AllLayers:
    def __init__(self, input_size, output_size, activation):
        self.activation = activation
        self.input_size = input_size
        self.output_size = output_size
        self.weights = []

    def propogate(self, input):
        output = np.dot(input, self.weights)
        output = self.activation(output)
        return output

    def set(self, weights):
        self.weights = weights


from simulation import Organism


class NeuralNetwork:
    def __init__(self, organism: Organism):
        self.layers = organism.network

    def propogate(self, input, weights):
        output = input
        for layer in self.layers:
            layer.set(weights)
            output = layer.propogate(output)
        return output
