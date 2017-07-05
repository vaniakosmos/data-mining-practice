import re
from pprint import pprint
from typing import List, Dict
import math


class Naive(object):
    def __init__(self):
        self.n_class = 0
        self.prob = {}
        self.init_prob = []

    def fit(self, xs, ys):
        self.n_class = max(ys) + 1

        for c in range(self.n_class):
            self.prob[c] = [0] * len(xs[0])

        c_counts = [0] * self.n_class

        for i, row in enumerate(xs):
            c = ys[i]
            for x, el in enumerate(row):
                self.prob[c][x] += el
                c_counts[c] += el

        for c, count in enumerate(c_counts):
            self.prob[c] = list(map(lambda x: self.smoothed_prob(x, count), self.prob[c]))

        self.init_prob = list(map(lambda count: sum(c_counts), c_counts))
        # self.init_prob = [.1, .1, 2, 2]

    def predict(self, xs) -> List[int]:
        ys = []
        for x in xs:
            res: List[Dict[str, int]] = []
            for c in range(self.n_class):
                r = math.log(self.init_prob[c])
                for i, e in enumerate(x):
                    r += math.log(self.prob[c][i]) * e
                res.append({'r': r, 'c': c})
            ys.append(max(res, key=lambda r: r['r'])['c'])
        return ys

    @staticmethod
    def smoothed_prob(a: int, b: int, k=1):
        return (a + k) / (b + 2*k)


def evaluate(gold, pred, n_class):
    cmat = [[0] * n_class for _ in range(n_class)]

    for i in range(len(gold)):
        a, b = gold[i], pred[i]
        cmat[a][b] += 1

    print('Confusion matrix:')
    for row in cmat:
        frow = ' '.join(map(lambda x: f'{x:2d}', row))
        print(f'[ {frow} ]')
    print()

    tp = [0] * n_class
    fp = [0] * n_class
    fn = [0] * n_class

    for y, row in enumerate(cmat):
        tp[y] = cmat[y][y]
        fn[y] = sum(row) - cmat[y][y]

    for x in range(n_class):
        c_sum = -cmat[x][x]
        for y in range(n_class):
            c_sum += cmat[y][x]
        fp[x] = c_sum

    print('true positives:', tp)
    print('false positives:', fp)
    print('false negatives:', fn)
    print()

    f1 = 0
    for i in range(n_class):
        if tp[i]:
            precision = tp[i] / (tp[i] + fp[i])
            recall = tp[i] / (tp[i] + fn[i])
            print(precision, recall)
            f1 += 2 * precision * recall / (precision + recall)
    f1 /= n_class

    print(f'f1-score: {f1 * 100:.3f}%')


def normalize(text):
    endings = 'а о у е і ий и ії'.split()

    text = text.lower()
    text = re.sub(r'[.-`\']', '', text)
    text = re.sub(r'[^а-яa-z-|=їіэ\s]', ' ', text)
    end_regex = '(' + '|'.join(endings) + ')$'
    end_regex = '|'.join('а о у е і и'.split())
    text = ' '.join([re.sub(end_regex, '', word) for word in text.split()])
    return text


def get_n_grams(words, n):
    grams = []
    for i in range(len(words)-1):
        grams.append(' '.join(words[i:i+n]))
    return grams


def build_dict():
    d = {}
    with open('data/train1.txt') as file:
        i = 0
        for line in file:
            words = line.split()[1:]
            words = normalize(' '.join(words)).split()
            # words = list(map(lambda w: normalize(w), words))
            for word in words:
                if word not in d:
                    d[word] = i
                    i += 1

            bi_gram = get_n_grams(words, 2)
            for gram in bi_gram:
                if gram not in d:
                    d[gram] = i
                    i += 1

            tri_gram = get_n_grams(words, 3)
            for gram in tri_gram:
                if gram not in d:
                    d[gram] = i
                    i += 1
    return d


def vectorize(words, d):
    vec = [0] * len(d)
    words = normalize(' '.join(words)).split()
    # words = list(map(lambda w: normalize(w), words))
    for word in words:
        if word in d:
            vec[d[word]] += 1

    # bi_gram = get_n_grams(words, 2)
    # for gram in bi_gram:
    #     if gram in d:
    #         vec[d[gram]] += 1
    #
    # tri_gram = get_n_grams(words, 3)
    # for gram in tri_gram:
    #     if gram in d:
    #         vec[d[gram]] += 1
    return vec


def extract_features(file_name, d):
    xs, ys = [], []
    with open(file_name, 'r') as file:
        for line in file:
            words = line.split()
            ys.append(int(words[0]))
            xs.append(vectorize(words[1:], d))
    return xs, ys


def main_task():
    d = build_dict()
    train_xs, train_ys = extract_features('data/train1.txt', d)
    test_xy, test_ys = extract_features('data/test1.txt', d)

    cl = Naive()
    cl.fit(train_xs, train_ys)
    res = cl.predict(test_xy)

    evaluate(test_ys, res, cl.n_class)


def test():
    train_xs, train_ys = [
                             [1, 1, 1, 0, 0, 0],
                             [1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1],
                             [0, 0, 1, 0, 1, 1]
                         ], [1, 1, 0, 0]
    test_xy, test_ys = [
                           [1, 0, 1, 0, 0, 0],
                           [1, 0, 0, 1, 1, 1]
                       ], [1, 0]

    cl = Naive()
    cl.fit(train_xs, train_ys)
    res = cl.predict(test_xy)
    evaluate(res, test_ys)


def main():
    main_task()


if __name__ == '__main__':
    main()
