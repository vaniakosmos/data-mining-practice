import math

from lab3.utils import Data


def euclid_dist(v1, v2):
    return math.sqrt(sum(map(
        lambda e: pow(e[0]-e[1], 2),
        zip(v1, v2))))


def determine_class(train_set, test, k):
    distances = []
    for row in train_set:
        features, clazz = row[:-1], row[-1]
        dist = euclid_dist(features, test)
        distances.append((dist, clazz))
    distances.sort(key=lambda x: x[0])
    distances = list(map(lambda x: x[1], distances[:k]))
    return max(set(distances), key=distances.count)


def evaluate(train: Data, test: Data, neighbours_number: int):
    confusion_matrix = [[0] * train.classes_number for _ in range(train.classes_number)]

    for row in test:
        features, clazz = row[:-1], row[-1]
        prediction = determine_class(train, features, neighbours_number)
        confusion_matrix[clazz][prediction] += 1
    return confusion_matrix
