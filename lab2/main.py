"""
Лабораторна робота No 2.
Пошук асоціативних правил

Побудуйте систему пошуку асоціативних правил алгоритмом apriori.
Перший рядок вхідного файлу містить два числа:
n – кількість транзакцій,
m – кількість об’єктів транзакцій (об’єкти визначаються номером від 0 до n-1).
Далі йде n рядків, кожен з яких містить ni – кількість елементів поточної транзакції і власне ni елементів.
Останній рядок вхідного файлу містить k – мінімальний порог достовірності.
Результуючий файл має містити списки елементів, з яких можна формувати асоціативні правила.
А також усі правила, для яких виконується умова conf(s ⇒ (F–s)) = supp(F)/supp(s)
не менше мінімального порогу достовірності.
"""


from typing import List, Dict, Tuple


def get_data() -> (int, int, List[Tuple[int, ...]]):
    with open('./data/input.txt', 'r') as file:
        ts = []
        for line in file:
            nums = [int(s) for s in line.split()]
            ts.append(nums)

        m = ts.pop(0)[0]
        k = ts.pop(0)[0]

        ts = [vectorise(t, m) for t in ts]
    return m, k, ts


def vectorise(elements: List[int], max_elem: int) -> Tuple[int, ...]:
    vec = [0] * max_elem
    for e in elements:
        vec[e] = 1
    return tuple(vec)


def contains(where: Tuple[int, ...], what: Tuple[int, ...]) -> bool:
    for i in range(len(what)):
        if what[i] == 1 and where[i] != 1:
            return False
    return True


def count_combos(combos: List[Tuple[int, ...]], ts: List[Tuple[int, ...]]) -> Dict[Tuple[int, ...], int]:
    counter = dict()
    for combo in combos:
        for transaction in ts:
            if contains(transaction, combo):
                counter[combo] = counter.get(combo, 0) + 1
    return counter


def filter_out(counter: Dict[Tuple[int, ...], int], k: int) -> List[Tuple[int, ...]]:
    combos = []
    for combo, count in counter.items():
        print(f"{combo} appears {count} time{'' if count == 1 else 's'}")
        if count >= k:
            combos.append(combo)
    print()
    return combos


def contains_enough_valid(combo: Tuple[int, ...], valid_combos: List[Tuple[int, ...]]) -> bool:
    n = sum(combo)
    for c in valid_combos:
        if contains(combo, c):
            n -= 1
        if n == 0:
            break
    return n == 0


def level_up_combos(valid_combos: List[Tuple[int, ...]], max_elem: int) -> List[Tuple[int, ...]]:
    out = set()
    for combo in valid_combos:
        for i in range(max_elem):
            if combo[i] == 0:
                new_combo = list(combo)
                new_combo[i] = 1
                new_combo = tuple(new_combo)
                if contains_enough_valid(new_combo, valid_combos):
                    out.add(new_combo)
    return list(out)


def apriori(m: int, k: int, ts: List[Tuple[int, ...]]):
    combos = [vectorise([e], m) for e in range(m)]

    while len(combos) != 0:
        print('= ' * 50)
        counters = count_combos(combos, ts)

        valid = filter_out(counters, k)
        print("Valid combos: \n{}\n".format('\n'.join(map(str, valid))))

        combos = level_up_combos(valid, m)
        print("New combos: \n{}\n".format('\n'.join(map(str, combos))))


def main():
    m, k, ts = get_data()
    apriori(m, k, ts)


if __name__ == '__main__':
    main()
