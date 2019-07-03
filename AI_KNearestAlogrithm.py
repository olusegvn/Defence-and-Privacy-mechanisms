import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import style
from collections import Counter

np.set_printoptions(threshold=np.inf)

# style.use('fivethirtyeight')

# data = {'k': [[2, 3, 2], [4, 3, 3]], 'r': [[3, 2, 5], [1, 0, 3]]}
# new = [2, 4, 1]


class Classifier:
    def __init__(self, data, opt='dict'):
        self.data = data
        self.vote = ''
        self.opt = opt
        self.pred = []

    def predict(self, predict, k=3):
        self.pred = predict
        if self.opt == 'dict':
            distance = []
            for group in self.data:
                for feature in self.data[group]:
                    euclidean_distance = np.linalg.norm(np.array(feature) - np.array(predict))
                    distance.append([euclidean_distance, group])
        if self.opt == 'list':
            distance = []
            for group in self.data:
                for feature in group[1]:
                    euclidean_distance = np.linalg.norm(np.array(feature) - np.array(predict))
                    distance.append([euclidean_distance, group[0]])

        votes = [i[1] for i in sorted(distance)[:k]]
        print("Top votes : ", votes)
        vote = Counter(votes).most_common(1)[0][0]
        print("Vote: ", vote)
        self.vote = vote
        return vote

    def show(self):
        for i in self.data:
            for j in i[1]:
                print(j)
                plt.scatter(j[0], j[1], color=i)
                plt.scatter(self.pred[0], self.pred[1], color=self.vote)

        plt.show()

    def check_accuracy(self, test_set):
        correct = 0
        total = 0
        self.data = test_set
        for group in test_set:
            for data in test_set[group]:
                vote = self.predict(data, k=5)
                if group == vote:
                    correct += 1
                total += 1
        return correct/total

