import math
from lab3.utils import *


def euclid_dist(v1, v2):
    return math.sqrt(sum(map(
        lambda e: pow(e[0]-e[1], 2),
        zip(v1, v2))))


def determine_class(train_set, test, k):
    distances = []
    for features, clazz in train_set:
        dist = euclid_dist(features, test)
        distances.append((dist, clazz))
    distances.sort(key=lambda x: x[0])
    distances = list(map(lambda x: x[1], distances[:k]))
    return max(set(distances), key=distances.count)


def evaluate(train, test, classes_number, neighbours_number):
    confusion_matrix = [[0] * classes_number for _ in range(classes_number)]

    for features, clazz in test:
        prediction = determine_class(train, features, neighbours_number)
        confusion_matrix[clazz][prediction] += 1

    print("Confusion Matrix:")
    print("\n".join(map(str, confusion_matrix)))
    print(f"Macro f1-score: {macro_f1_score(confusion_matrix)}")
    print(f"Micro f1-score: {micro_f1_score(confusion_matrix)}")
    print()


if __name__ == '__main__':
    evaluate()
