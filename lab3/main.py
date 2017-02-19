"""
Лабораторна робота No3.
Класифікація даних

 Побудувати класифікатор на основі:
1. дерева рішень
2. k-means
3. методу найближчого сусіда
Навчити та оцінити точність класифікатора принаймни на трьох бд (https://archive.ics.uci.edu/ml/datasets.html).
"""
from lab3 import k_nearest_neighbours, decision_tree, k_means
from utils_pack.printers import *
from lab3.utils import Data


def main():
    headers_length = 50

    data_sets = (
        ("IRIS", "./data_sets/iris.csv"),
        ("WINE", "./data_sets/wine.csv"),
        ("GLASS", "./data_sets/glass.csv"),
    )

    for name, file in data_sets:
        print_title(name, length=50)

        data_set = Data(csv=file)
        train, test = data_set.split_randomly(ratio=0.7)

        print_header("Decision Tree", length=headers_length)
        confusion_matrix = decision_tree.evaluate(train, test, max_depth=11, print_out_tree=False)
        print_results(confusion_matrix)

        print_header("K-Means", length=headers_length)
        confusion_matrix = k_means.evaluate(train, test)
        print_results(confusion_matrix)

        print_header("K-Nearest Neighbours", length=headers_length)
        confusion_matrix = k_nearest_neighbours.evaluate(train, test, neighbours_number=3)
        print_results(confusion_matrix)


if __name__ == '__main__':
    main()
