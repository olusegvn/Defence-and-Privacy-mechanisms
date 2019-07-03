# NeuralNet


import numpy as np
import math
import pickle

X = np.array([[123, 121, 111], [112, 154, 155], [144, 121, 135], [123, 111, 143], [121, 111, 111]])
x = [1 / (1 + np.e ** -x) for x in X]
Y = np.array([[110, 111, 122, 121, 113]])
y = [1 / (1 + np.e ** -x) for x in Y]
y = y.reshape(5, 1)
print(y)
epochs = 60000

X = x[0].shape[0]


def sigmoid(x):
    return 1 / (1 + np.e ** -x)


def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


weight1 = np.random.rand(3, 1)
weight2 = np.random.rand(1, 1)
bias = np.random.rand(1)


class NeuralNetwork:
    def __init__(self, x, y, weight1, weight2, bias):
        self.input = x
        self.weight1 = weight1
        self.weight2 = weight2
        self.y = y
        self.bias = bias
        self.lr = 0.01

    def feedForward(self):
        self.layer1 = np.dot(self.input, self.weight1) + self.bias
        self.l1 = sigmoid(self.layer1)
        self.layer2 = np.dot(self.l1, self.weight2) + self.bias
        self.z = sigmoid(self.layer2)

    def backPropagation(self):
        error = self.z - self.y
        loss = error.sum()
        print(loss)
        if error.sum() >= 1:
            pass

##        d1 = error * self.l1
##        d2 = np.dot(d1, self.weight1.T)
        d3 = sigmoid_der(self.l1)
        d4 = error * d3
        d5 = np.dot(self.input.T, d4)

        d6 = error * self.z
        d7 = self.l1.T
        d8 = np.dot(d7, d6)

        self.weight1 -= d5
        self.weight2 -= d8

        for num in d6:
            self.bias -= self.lr * num

    def returnWeightsandBiases(self):
        return self.weight1, self.weight2, self.bias

    def predict(self, prediction):
        self.pred = np.array(prediction)
        result = np.dot(self.pred, self.weight1) + self.bias
        result = math.ceil(result)
        return result


if __name__ == '__main__':
    NN2 = NeuralNetwork(x,y,weight1,weight2,bias)
    for i in range(epochs):
        NN2.feedForward()
        NN2.backPropagation()
    print(NN2.predict(np.array([123, 121, 0])))
