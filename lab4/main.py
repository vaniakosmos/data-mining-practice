"""
Лабораторна робота No4.
Кластеризація даних

Побудувати систему, що розбиває вхідні дані на певну кількість кластерів методом:
1. k-means
2. найбліжчого сусіда
"""
from lab4.utils import get_data, plot
from lab4.k_means import k_means
from lab4.k_nearest_neighbours import k_nearest_neighbours
from lab4.nn import nn1, nn2


def main():
    data = get_data(file_name='./data/pyramid.data')
    # data = get_data(file_name='./data/spiral.data')

    clusters, centers = k_means(data, k=2)
    plot(clusters, centers, "k-means")

    clusters, centers = nn1(data, limit=1)
    plot(clusters, centers, "original kNN")

    clusters, centers = nn2(data, limit=1)
    plot(clusters, centers, "original kNN")

    clusters, centers = k_nearest_neighbours(data, k=2)
    plot(clusters, centers, "k-nearest-neighbours")


if __name__ == '__main__':
    main()
