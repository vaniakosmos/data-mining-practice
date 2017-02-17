from lab3.utils import Data


def gini_index(groups: tuple, classes_number: int):
    gini = 0.0
    for class_value in range(classes_number):
        for group in groups:
            size = len(group)
            if size == 0:
                continue
            proportion = [row[-1] for row in group].count(class_value) / size
            gini += (proportion * (1.0 - proportion))
    return gini


def split(index: int, value: float, data_set: Data):
    left, right = [], []
    for row in data_set:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return Data(list=left, source=data_set), Data(list=right, source=data_set)


# get split with minimal gini index
def get_split(data_set: Data):
    b_index, b_value, b_score, b_groups = [None] * 4

    for index in range(data_set.features_number):
        for row in data_set:
            groups = split(index, row[index], data_set)
            gini = gini_index(groups, data_set.classes_number)

            if b_score is None or gini < b_score:
                b_index, b_value, b_score, b_groups = index, row[index], gini, groups
    return {'index': b_index, 'value': b_value, 'groups': b_groups}


def leaf(group: Data):
    ys = group.ys
    return max(set(ys), key=ys.count)


def tree_split(node: dict, max_depth: int, min_size: float, depth: int):
    left, right = node['groups']
    del (node['groups'])

    # check for a no split
    if not left or not right:
        node['left'] = node['right'] = leaf(left + right)
        return

    # check for max depth
    if depth >= max_depth:
        node['left'], node['right'] = leaf(left), leaf(right)
        return

    # process left child
    if len(left) <= min_size:
        node['left'] = leaf(left)
    else:
        node['left'] = get_split(left)
        tree_split(node['left'], max_depth, min_size, depth + 1)

    # process right child
    if len(right) <= min_size:
        node['right'] = leaf(right)
    else:
        node['right'] = get_split(right)
        tree_split(node['right'], max_depth, min_size, depth + 1)


def build_tree(data_set: Data, max_depth: int, min_size: float):
    root = get_split(data_set)
    tree_split(root, max_depth, min_size, 1)
    return root


def print_tree(node: dict, depth=0):
    delimiter = '|   '
    if isinstance(node, dict):
        print("{}+ [x{} < {:.3f}]".format(
            delimiter * depth,
            node['index'] + 1,
            node['value']))

        print_tree(node['left'], depth + 1)
        print_tree(node['right'], depth + 1)
    else:
        print('{}[{}]'.format(
            delimiter * depth,
            node))


def predict(node: dict, row: list):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']


def evaluate(train: Data, test: Data, max_depth=3, print_out_tree=False):
    tree = build_tree(train, max_depth=max_depth, min_size=1)

    if print_out_tree:
        print_tree(tree)

    confusion_matrix = [[0] * train.classes_number for _ in range(train.classes_number)]
    for row in test:
        prediction = predict(tree, row)
        confusion_matrix[row[-1]][prediction] += 1

    return confusion_matrix
