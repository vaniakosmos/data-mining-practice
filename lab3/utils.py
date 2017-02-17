import csv
import random


class Data(object):
    def __init__(self, **kwargs):
        self.__rows = []
        self.__classes_number = 0
        self.__classes_names = []

        if 'csv' in kwargs.keys():
            self.__get_rows(kwargs['csv'])
        elif 'list' in kwargs.keys() and 'source' in kwargs.keys():
            self.__rows = kwargs['list']
            self.__classes_number = kwargs['source'].classes_number
            self.__classes_names = kwargs['source'].classes_names
        else:
            raise ValueError("Incorrect Data initial parameter(s)")

    def __getitem__(self, row):
        return self.__rows[row]

    def __iter__(self):
        return iter(self.__rows)

    def __len__(self):
        return len(self.__rows)

    def __add__(self, other):
        return Data(list=(self.__rows + other.__rows), source=self)

    @property
    def features_number(self):
        return len(self.__rows[0]) - 1

    @property
    def ys(self):
        return [row[-1] for row in self.__rows]

    @property
    def xs(self):
        return [row[:-1] for row in self.__rows]

    @property
    def classes_number(self):
        return self.__classes_number

    @property
    def classes_names(self):
        return self.__classes_names

    def split_randomly(self, ratio=0.7) -> tuple:
        train, test = [], []
        for row in self.__rows:
            if random.random() < ratio:
                train.append(row)
            else:
                test.append(row)
        return Data(list=train, source=self), Data(list=test, source=self)

    def split_fairly(self, ratio=0.7):
        train, test = [], []
        groups = [[] for _ in range(self.classes_number)]
        for row in self.__rows:
            groups[row[-1]].append(row)
        for group in groups:
            limit = int(len(group) * ratio)
            train += group[:limit]
            test += group[limit:]
        return Data(list=train, source=self), Data(list=test, source=self)

    def print(self):
        print("\n".join(map(lambda row: f"{row[:-1]} > {row[-1]}", self.__rows)))

    def __get_rows(self, csv_file):
        reader = csv.reader(open(csv_file), delimiter=',')
        self.__classes_number = 0
        classes = {}
        for row in reader:
            c = row[-1]
            if c not in classes.keys():
                classes[c] = self.classes_number
                self.__classes_number += 1
                self.classes_names.append(c)
            self.__rows.append(list(map(float, row[:-1])) + [classes[c]])
