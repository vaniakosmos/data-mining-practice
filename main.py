import unittest
from random import random, randint
import math

from typing import Iterable


def func(nums: Iterable[float]) -> float:
    return math.sqrt(sum(n*n for n in nums))


def gen():
    with open('data.txt', 'w') as file:
        for _ in range(10):
            r = randint(3, 6)
            vec = []
            for i in range(r):
                num = round(random() * 30, 3)
                vec.append(num)
            res = round(func(vec), 6)
            vec.append(res)
            file.write(' '.join(map(str, vec)))
            file.write('\n')


# створюємо клас для тестування
class TestFunc(unittest.TestCase):
    # створюєму функцію для тестування якоїсь конкретної фічі
    def test_with_data_table(self):
        # відкриваємо файл
        with open('data.txt', 'r') as file:
            # зчитуємо стічку з файлу
            for line in file:
                # відкидаємо зайві переноси та пробіли
                line = str.strip(line)
                # ковертуєму стрічку в масив чисел
                nums = list(map(float, line.split()))
                # передаємо в res останнє число, а все інше в vec
                vec, res = nums[:-1], nums[-1]
                # шукаємо що ж поверне наша функція
                func_res = func(vec)
                # записуємо в консоль результати розрахунків і ті що ми очікуємо
                print(func_res, res)
                # перевіряємо чи рівні числа (до 3 знаку після коми)
                self.assertAlmostEqual(func_res, res, places=3)


if __name__ == '__main__':
    unittest.main()
