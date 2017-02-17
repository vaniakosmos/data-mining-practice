def f1_score(tp, fp, fn):
    try:
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        return 2 * precision * recall / (precision + recall) if tp != 0 else 0
    except ZeroDivisionError:
        return 0


def macro_f1_score(confusion_matrix):
    res = 0
    classes_count = len(confusion_matrix)
    for i in range(classes_count):
        tp = confusion_matrix[i][i]
        fn = sum(confusion_matrix[i]) - tp
        fp = sum([row[i] for row in confusion_matrix]) - tp
        res += f1_score(tp, fp, fn) / classes_count
    return res


def micro_f1_score(confusion_matrix):
    # fn and fp will be the same
    tp, fn = 0, 0
    classes_count = len(confusion_matrix)
    for i in range(classes_count):
        tp += confusion_matrix[i][i]
        fn += sum(confusion_matrix[i]) - confusion_matrix[i][i]
    return f1_score(tp, fn, fn)
