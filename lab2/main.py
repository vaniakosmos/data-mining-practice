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
    for i, line in enumerate(open("./data/input.txt").readlines()):
        ts.append(list(map(int, line.split())))
    m = ts.pop(0)[0]
    k = ts.pop()[0]
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
    return out


def count_combos(valid, ts):
    counter = dict(zip(
        [tuple(combo) for combo in valid],
        [0]*len(valid)))
    for combo in valid:
        for transaction in ts:
            if contains(transaction, combo):
                counter[tuple(combo)] += 1
    return counter


def contains(where, what):
    yes = True
    for e in what:
        yes = yes and (e in where)
    return yes


def filter_valid(bad, combos) -> list:
    valid = []
    for combo in combos:
        ok = True
        for b in bad:
            ok = ok and not contains(what=b, where=combo)
        if ok:
            valid.append(combo)
    return valid


def save(out: dict):
    f = open("./data/output.txt", "w")
    for key, value in out.items():
        f.write(f"{key} :  {value}\n")
    f.close()


def apriori(m: int, k: int, ts: list):
    out = dict()
    valid = [{e} for e in range(m)]
    while len(valid) != 0:
        counter = count_combos(valid, ts)

        # add if only over threshold
        good = []
        bad = []
        for i in range(len(valid)):
            combo = valid[i]
            count = counter[tuple(combo)]
            print(f"{combo} appears {count} time{'' if count == 1 else 's'}")
            if counter[tuple(combo)] >= k:
                good.append(combo)
                out[tuple(combo)] = counter[tuple(combo)]
            else:
                bad.append(combo)
        print()

        print("Good: {}\n".format(good))
        combos = get_combo(m, good)

        valid = filter_valid(bad, combos)
        print(f"New combos: {valid}\n")
    save(out)


def main():
    m, k, ts = get_data()
    apriori(m, k, ts)


if __name__ == '__main__':
    main()
