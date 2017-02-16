"""
Лабораторна робота No3.
Класифікація даних

 Побудувати класифікатор на основі:
1. дерева рішень
2. k-means
3. методу найближчого сусіда
Навчити та оцінити точність класифікатора принаймни на трьох бд (https://archive.ics.uci.edu/ml/datasets.html).
"""
from lab3 import k_nearest_neighbours, decision_tree
from utils_pack.printers import *
from lab3.utils import Data


def main():
    data_sets = (
        ("IRIS", "./datasets/iris.csv"),
        # ("BALANCE SCALE", "./datasets/balance.csv"),
        ("WINE", "./datasets/wine.csv"),
        ("GLASS", "./datasets/glass.csv"),
    )

    for name, file in data_sets:
        print_title(name)

        data_set = Data(csv=file)
        train, test = data_set.split_randomly(ratio=0.7)

        print_header("K-Nearest Neighbours")
        k_nearest_neighbours.evaluate(train, test, data_set.classes_number, neighbours_number=3)

        # print_header("Decision Tree")
        # decision_tree.evaluate(train, test, data_set.classes_number)


if __name__ == '__main__':
    main()
