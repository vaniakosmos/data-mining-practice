import csv
import random


def f1_score(tp, fp, fn):
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * precision * recall / (precision + recall) if tp != 0 else 0


def macro_f1_score(confusion_matrix):
    res = 0
    classes_count = len(confusion_matrix)
    for i in range(classes_count):
        tp = confusion_matrix[i][i]
        fn = sum(confusion_matrix[i]) - tp
        fp = sum([row[i] for row in confusion_matrix]) - tp
        res += f1_score(tp, fp, fn) / classes_count
    return res


def micro_f1_score(confusion_matrix):
    # fn and fp will be the same
    tp, fn = 0, 0
    classes_count = len(confusion_matrix)
    for i in range(classes_count):
        tp += confusion_matrix[i][i]
        fn += sum(confusion_matrix[i]) - confusion_matrix[i][i]
    return f1_score(tp, fn, fn)


class Data(object):
    def __init__(self, **kwargs):
        if 'csv' in kwargs.keys():
            self.__rows = []
            self.__get_rows(kwargs['csv'])
        elif 'list' in kwargs.keys():
            self.__rows = kwargs['list']
        else:
            pass

    def __get_rows(self, csv_file):
        reader = csv.reader(open(csv_file), delimiter=',')
        self.classes_number = 0
        classes = {}
        for row in reader:
            c = row[-1]
            if c not in classes.keys():
                classes[c] = self.classes_number
                self.classes_number += 1
            self.__rows.append(list(map(float, row[:-1])) + [classes[c]])

    def __getitem__(self, row):
        return self.__rows[row][:-1], self.__rows[row][-1]

    def get_features(self, index) -> list:
        return self.__rows[index][:-1]

    def get_class(self, index) -> int:
        return self.__rows[index][-1]

    def split_randomly(self, ratio=0.7) -> tuple:
        train, test = [], []
        for row in self.__rows:
            if random.random() < ratio:
                train.append(row)
            else:
                test.append(row)
        return Data(list=train), Data(list=test)

    def split_fair(self, ratio=0.7):
        pass

    def __len__(self):
        return len(self.__rows)

    def print(self):
        print("\n".join(map(lambda row: f"{row[:-1]} > {row[-1]}", self.__rows)))
