"""
Лабораторна робота No 5.
Text Mining

Побудуйте класифікатор текстових повідомлень використовуючи алгоритм наївного баєсівського класифікатора і
SMS Spam Collection (http://www.dt.fee.unicamp.br/~tiago/smsspamcollection/) з accuracy > 85%.
"""
import re
from math import log, exp
from utils_pack.measurments import f1_score


def normalize(sentence: str):
    sentence = re.sub(r"[^\w\s]", "", sentence)
    return sentence.split()


def get_data():
    data = []
    for line in open("data/spam.txt"):
        words = line.split()
        data.append({"class": words[0],
                     "text": normalize(" ".join(words[1:]))})
    return data


def smoothing(a: int, b: int, k=1):
    return a + k, b + 2*k


def build_vocabulary(data: list):
    vocabulary = {}
    spam_number = 0
    for message in data:
        for word in message['text']:
            if word not in vocabulary:
                vocabulary[word] = (0, 0)

        if message['class'] == '3':
            spam_number += 1
            for word in message['text']:
                s, a = vocabulary[word]
                vocabulary[word] = s + 1, a + 1
        else:
            for word in message['text']:
                s, a = vocabulary[word]
                vocabulary[word] = s, a + 1
    return vocabulary, spam_number / len(data)


def split(data: list, ratio=0.8):
    limit = int(len(data) * ratio)
    return data[:limit], data[limit:]


def predict(voc: dict, text: list, spam_prob: float):
    prediction = log(spam_prob / (1.0 - spam_prob))
    for word in text:
        if word in voc:
            s, a = voc[word]
            s, a = smoothing(s, a)
            prediction += log(s / (a - s))
    return bound_in_zero_one(prediction)


def bound_in_zero_one(q):
    return 1 if q > 100 else exp(q) / (1 + exp(q))


def evaluate(voc: dict, test: list, spam_prob: float):
    tp, fp, fn = 0, 0, 0
    for message in test:
        prediction = predict(voc, message['text'], spam_prob)
        prediction_class = 'spam' if prediction >= 0.5 else 'ham'
        if prediction_class == message['class']:
            tp += 1
        elif prediction_class == 'spam':
            fp += 1
        elif prediction_class == 'ham':
            fn += 1
        # print(f"{' '.join(message['text'])}\nClass: {message['class']}, Prediction: {prediction_class}\n\n")
    print(f"F1-score: {f1_score(tp, fp, fn)}\n")


def get_data2():
    train = []
    test = []

    with open('./data/train.txt') as file:
        for line in file:
            words = line.strip().split()
            train.append({'class': words[0], 'text': words[1:]})

    with open('./data/test.txt') as file:
        for line in file:
            words = line.strip().split()
            test.append({'class': words[0], 'text': words[1:]})

    return train, test


def main():
    # train, test = split(get_data(), ratio=0.9)
    train, test = get_data2()
    # print(test)

    vocabulary, spam_prob = build_vocabulary(train)

    evaluate(vocabulary, test, spam_prob)


if __name__ == '__main__':
    main()
