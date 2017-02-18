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
        print(f"Centers: [{', '.join(['(%.2f, %.2f)' % e for e in centers])}]")

        iterations += 1
        changed = False
        clusters = [[] for _ in range(k)]

        distribute(data, k, clusters, centers)

        reassign_centers(k, clusters, centers)

        mask, changed = check_changes(mask, centers, changed)

    print(f"Iterations: {iterations}")

    return clusters, centers


def distribute(data: iter, k: int, clusters: iter, centers: iter):
    for dot in data:
        chosen_cluster_id, min_dist = None, None
        for cluster_id in range(k):
            d = dist(centers[cluster_id], dot)
            if min_dist is None or d < min_dist:
                chosen_cluster_id = cluster_id
                min_dist = d
        clusters[chosen_cluster_id].append(dot)


def reassign_centers(k: int, clusters: iter, centers: iter):
    for i in range(k):
        cluster = clusters[i]
        sx = sum(e[0] for e in cluster) / len(cluster)
        sy = sum(e[1] for e in cluster) / len(cluster)
        centers[i] = sx, sy


def check_changes(mask: iter, centers: iter, changed: bool):
    if mask is None or set(mask) != set(centers):
        changed = True
    mask = list(centers)
    return mask, changed
