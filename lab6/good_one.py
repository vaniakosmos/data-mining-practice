import re
from pprint import pprint
from typing import List, Dict
from collections import Counter

from math import log


class Naive(object):
    def __init__(self):
        self.classes = []
        self.all_features = set()
        self.probs = {}
        self.init_prob = {}

    @property
    def n_classes_(self):
        return len(self.classes)

    def fit(self, sents, labels):
        self.classes = list(set(labels))

        # count all features
        for label, sent in zip(labels, sents):
            features = self.featurise(sent)
            for f in features:
                self.all_features.add(f)

        self.probs = {}
        c_count = Counter(labels)

        for label in self.classes:
            self.probs[label] = Counter()

        for label, sent in zip(labels, sents):
            features = self.featurise(sent)
            self.probs[label] += features

        for label in self.classes:
            for feature in self.all_features:
                c = self.probs[label][feature]
                self.probs[label][feature] = self.smoothed_prob(c, c_count[label])

        size = len(labels)
        self.init_prob = {label: c_count[label] / size for label in self.classes}
        # self.init_prob = [.1, .1, 2, 2]

    def predict(self, sents) -> List[str]:
        ys = []
        for sent in sents:
            features = self.featurise(sent)
            res: List[Dict[str, int]] = []
            for label in self.classes:
                r = log(self.init_prob[label])
                for key in features:
                    if key in self.all_features:
                        r += log(self.probs[label][key] * features[key])
                res.append({'r': r, 'c': label})
            ys.append(max(res, key=lambda rs: rs['r'])['c'])
        return ys

    @staticmethod
    def smoothed_prob(a: int, b: int, k=1):
        return (a + k) / (b + 2*k)

    def featurise(self, sent) -> Counter:
        words = self.normalize(sent).split()
        return Counter(words + self.get_n_grams(words, 2) + self.get_n_grams(words, 3))

    @staticmethod
    def get_n_grams(words, n):
        grams = []
        for i in range(len(words) - 1):
            grams.append(' '.join(words[i:i + n]))
        return grams

    @staticmethod
    def normalize(text):
        endings = 'а о у е і ий и ії'.split()
        text = text.lower()
        text = re.sub(r'[.-`]', '', text)
        text = re.sub(r'[^а-яa-z-|=їіэ\s]', ' ', text)
        end_regex = '(' + '|'.join(endings) + ')$'
        end_regex = '|'.join('а о у е і и'.split())
        # noinspection PyTypeChecker
        text = ' '.join([
            re.sub(end_regex, '', word) if len(word) > 2 else word
            for word in text.split()])
        return text


def get_data(file_name):
    """
    :param file_name: 
    :return: Tuple[
                List[sentence], 
                List[label]
             ]
    """
    xs = []
    ys = []
    with open(f'./data/{file_name}', 'r') as file:
        i = -1
        got_class = False
        curr_class = None
        for line in file:
            line = line.strip()
            if i > 0:
                i -= 1
                xs.append(line)
                ys.append(curr_class)
                if i <= 0:
                    got_class = False
            elif line and got_class:
                i = int(line)
            elif line:
                curr_class = line
                got_class = True
    return xs, ys


def evaluate(gold, pred, classes):
    n_class = len(classes)
    cmat = [[0] * n_class for _ in range(n_class)]

    for i in range(len(gold)):
        a, b = gold[i], pred[i]
        a = classes.index(a)
        b = classes.index(b)
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


def main():
    bad_variant = False
    if not bad_variant:
        train_xs, train_ys = get_data('train.txt')
        test_xs, test_ys = get_data('test.txt')
    else:
        train_xs, train_ys = get_data('train-full.txt')
        test_xs, test_ys = get_data('test-full.txt')

    clf = Naive()
    clf.fit(train_xs, train_ys)

    pred_y = clf.predict(test_xs)

    for label, sent in zip(pred_y, test_xs):
        print(label)
        print(sent)
        print()

    cls = clf.classes
    if bad_variant:
        cls2 = list(set(test_ys))
        for c in cls2:
            if c not in cls:
                cls.append(c)

    evaluate(test_ys, pred_y, cls)


if __name__ == '__main__':
    main()
