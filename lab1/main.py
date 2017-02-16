"""
Лабораторна робота No 1.
Map-Reduce алгоритм

Розробити алгоритми map-reduce для обробки послідовності чисел.
Вхідний файл data.txt містить послідовність чисел.
Результуючі файли мають містити:
1. найбільше число послідовності
2. середнє значення всіх чисел
3. той самий набір чисел, але кожне число в ньому зустрічається один раз .
4. кількість різних чисел у файлі
"""

from random import randint

from utils_pack.printers import print_title
from lab1.tasks.maximum import MaximumMapReduce
from lab1.tasks.average import AverageMapReduce
from lab1.tasks.unique import UniqueMapReduce
from lab1.tasks.unique_number import NumberOfUniqueMapReduce


def generate_file(num=10, file_name="input.txt"):
    f = open(file_name, "w")
    for i in range(num):
        nums_in_seq = randint(100, 1000)
        min_value = randint(-1000, 1000)
        max_value = min_value + randint(0, 1000)
        f.write(" ".join(map(str, generate_sequence(nums_in_seq, min_value, max_value))))
        f.write("\n")
    f.close()


def generate_sequence(num=1000, min_value=0, max_value=1000) -> list:
    res = [0]*num
    for i in range(num):
        res[i] = randint(min_value, max_value)
    return res


def main():
    tasks = (("MAXIMUM", MaximumMapReduce()),
             ("AVERAGE", AverageMapReduce()),
             ("UNIQUE", UniqueMapReduce()),
             ("NUMBER OF UNIQUE", NumberOfUniqueMapReduce()))

    for title, task in tasks:
        print_title(title)
        for line in open("./data/input.txt", "r").readlines():
            seq = list(map(int, line.split()))
            task.calculate(seq)

if __name__ == "__main__":
    main()
