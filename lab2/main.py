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


def get_data() -> (int, int, list):
    ts = []
    for i, line in enumerate(open("input.txt").readlines()):
        ts.append(list(map(int, line.split())))
    m = ts.pop(0)[0]
    k = ts.pop()[0]
    print(m, k, ts)
    return m, k, ts


def get_combo(m: int, ts: list) -> list:
    out = []
    for i in range(len(ts)):
        ts[i] = list(ts[i])

    for i in range(m):
        for t in ts:
            if i not in t:
                out.append(set(t + [i]))

    used = []
    out = [x for x in out if x not in used and (used.append(x) or True)]
    print(out)
    return out


def apriori(m: int, k: int, ts: list):
    out = dict()
    valid = [{e} for e in range(m)]
    while len(valid) != 0:
        # count
        for combo in valid:
            for transaction in ts:
                ok = True
                for e in combo:
                    ok = ok and (e in transaction)
                print("{} in {} ? {}".format(combo, transaction, ok))
                if ok:
                    if tuple(combo) not in out:
                        out[tuple(combo)] = 0
                    out[tuple(combo)] += 1

        # remove if under threshold
        very_valid = []
        for i in range(len(valid)):
            combo = valid[i]
            print("{} count {}".format(combo, out[tuple(combo)]))
            if out[tuple(combo)] < k:
                out.pop(tuple(combo), None)
            else:
                very_valid.append(combo)

        print("Good: {}".format(very_valid))
        valid = get_combo(m, very_valid)
    save(out)


def save(out: dict):
    f = open("output.txt", "w")
    for key, value in out.items():
        f.write("{} :  {}\n".format(str(key), str(value)))
    f.close()


def main():
    m, k, ts = get_data()
    apriori(m, k, ts)


if __name__ == '__main__':
    main()
