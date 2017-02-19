import random
from lab4.utils import dist


def k_means(data: list, k=3):
    init_dot_indexes = random.sample(range(len(data)), k)
    # init_dot_indexes = [1, 401, 601]

    clusters, mask = None, None

    centers = [data[i] for i in init_dot_indexes]
    changed = True
    iterations = 0

    while changed:
        # print(f"Centers: [{', '.join(['(%.2f, %.2f)' % e for e in centers])}]")

        iterations += 1
        changed = False
        clusters = [[] for _ in range(k)]

        distribute(data, k, clusters, centers)

        reassign_centers(clusters, centers)

        mask, changed = check_changes(mask, centers, changed)

    print(f"Iterations: {iterations}")

    return clusters, centers


def distribute(data: iter, k: int, clusters: iter, centers: iter):
    for vector in data:
        chosen_cluster_id, min_dist = None, None
        for cluster_id in range(k):
            d = dist(centers[cluster_id], vector)
            if min_dist is None or d < min_dist:
                chosen_cluster_id = cluster_id
                min_dist = d
        clusters[chosen_cluster_id].append(vector)


def reassign_centers(clusters: iter, centers: iter):
    features_number = len(clusters[0][0])
    for i, cluster in enumerate(clusters):
        sum_vector = [sum(e[j] for e in cluster) for j in range(features_number)]
        vector = [sum_vector[j] / len(cluster) for j in range(features_number)]
        centers[i] = tuple(vector)


def check_changes(mask: iter, centers: iter, changed: bool):
    if mask is None or set(mask) != set(centers):
        changed = True
    mask = list(centers)
    return mask, changed
