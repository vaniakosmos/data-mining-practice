from random import random
import matplotlib.pyplot as plt


def rect(center, width, height, size=1000):
    cx, cy = center
    heap = [None] * size
    for i in range(size):
        x, y = random() * width, random() * height
        heap[i] = cx + x - width/2, cy + y - height/2
    return heap


def spiral(center, steps_number, step, size=1000, width=0.2, clockwise=True):
    curr_step = 0
    curr_center = center
    cw = (1, 2) if clockwise else (3, 0)
    heap = []
    for i in range(steps_number):
        curr_step += step

        cx, cy = curr_center
        if i % 2 == 1:
            cx += curr_step * (1 if i % 4 == cw[0] else -1)
        else:
            cy += curr_step * (1 if i % 4 == cw[1] else -1)

        heap_size = 2 * size * (i + 1) // (steps_number * (steps_number-1))
        heap_center = (cx + curr_center[0]) / 2, (cy + curr_center[1]) / 2

        if i % 2 == 0:
            heap += rect(heap_center, width, curr_step, size=heap_size)
        else:
            heap += rect(heap_center, curr_step, width, size=heap_size)

        curr_center = cx, cy
    return heap


def save(heap, file):
    for coord in heap:
        file.write(f"{coord}\n")


def plot(data_file):
    xs, ys = [], []

    for dot in open(data_file, 'r').readlines():
        x, y = eval(dot)
        xs.append(x)
        ys.append(y)

    plt.plot(xs, ys, 'o')
    # plt.axis([0, 6, 0, 20])
    plt.show()


def make_pyramid(file_name='./data/pyramid.data', show=False):
    file = open(file_name, 'w')

    heap = []
    heap += rect((0, 0), 4, 1, size=400)
    heap += rect((0, 2), 2, 1, size=200)
    heap += rect((0, 4), 1, 1, size=100)
    save(heap, file)
    file.close()

    if show:
        plot(file_name)


def make_spiral(file_name='./data/spiral.data', show=False):
    file = open(file_name, 'w')

    heap = []
    heap += spiral((-2, 0), 20, 4, clockwise=True, size=2000)
    heap += spiral((2, 0), 20, 4, clockwise=False, size=2000)
    save(heap, file)
    file.close()

    if show:
        plot(file_name)


def main():
    make_spiral(show=True)


if __name__ == '__main__':
    main()
