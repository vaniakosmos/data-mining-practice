from random import random
import matplotlib.pyplot as plt


def split(data, x_index=0, y_index=1):
    xs, ys = [], []
    for vector in data:
        x, y = vector[x_index], vector[y_index]
        xs.append(x)
        ys.append(y)
    return xs, ys


def bind_color(color, start=0.3, length=0.6):
    return start + color * length


def plot(clusters: list, centers: list, title=""):
    colors = [(bind_color(random()),
               bind_color(random()),
               bind_color(random()))
              for _ in range(len(clusters))]

    for color, cluster in zip(colors, clusters):
        xs, ys = split(cluster)
        plt.plot(xs, ys, 'o', c=color)

    if centers is not None:
        plt.plot(*split(centers), 'x', c='black', markersize=10)
    plt.title(title)
    plt.show()


def get_data(file_name='./data/pyramid.data'):
    data = []
    for line in open(file_name, 'r'):
        data.append(eval(line))
    return data


def euclid_dist(v1, v2):
    return sum([pow(a-b, 2) for a, b in zip(v1, v2)])


def dist(v1, v2):
    return euclid_dist(v1, v2)
