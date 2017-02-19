from lab3.utils import Data


def predict(vector, groups):
    chosen_class, min_changes = None, None
    for index, group in enumerate(groups):
        sum_vector, size = group
        old_center = [e / size for e in sum_vector]
        new_center = [(a + b) / (size + 1) for a, b in zip(sum_vector, vector)]

        change = sum([pow(a-b, 2) for a, b in zip(old_center, new_center)])

        if min_changes is None or change < min_changes:
            chosen_class = index
            min_changes = change
    return chosen_class


def calculate_sums(data: Data):
    groups = [[[0 for _ in range(len(data[0])-1)], 0] for _ in range(data.classes_number)]
    for instance in data:
        vector, class_id = instance[:-1], instance[-1]
        sum_vector, size = groups[class_id]
        sum_vector = [a+b for a, b in zip(sum_vector, vector)]
        size += 1
        groups[class_id] = sum_vector, size
    return groups


def evaluate(train: Data, test: Data):
    confusion_matrix = [[0] * train.classes_number for _ in range(train.classes_number)]

    groups = calculate_sums(train)
    for instance in test:
        vector, class_id = instance[:-1], instance[-1]
        prediction = predict(vector, groups)

        confusion_matrix[class_id][prediction] += 1

    return confusion_matrix
