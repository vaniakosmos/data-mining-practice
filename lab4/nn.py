import random

import time

from lab4.utils import dist


def nn1(data: list, limit: float):
    vec = random.sample(data, 1)[0]
    data.remove(vec)
    clusters = [[vec]]

    while len(data) > 0:
        for vector1 in data:
            chosen_cluster, min_dist = None, None
            for cluster_id, cluster in enumerate(clusters):
                for vector2 in cluster:
                    d = dist(vector1, vector2)
                    if min_dist is None or d < min_dist:
                        chosen_cluster = cluster_id
                        min_dist = d
            if min_dist > limit:
                clusters.append([])
                clusters[-1].append(vector1)
            else:
                clusters[chosen_cluster].append(vector1)
            data.remove(vector1)

    return clusters, None


def nn2(data: list, limit: float):
    vec = random.sample(data, 1)[0]
    data.remove(vec)
    clusters = [[vec]]

    start = time.time()

    while len(data) > 0:
        chosen_vector, chosen_cluster, min_dist = None, None, None
        for vector1 in data:
            chosen_cluster, min_dist = None, None
            for cluster_id, cluster in enumerate(clusters):
                for vector2 in cluster:
                    d = dist(vector1, vector2)
                    if min_dist is None or d < min_dist:
                        chosen_cluster = cluster_id
                        chosen_vector = vector1
                        min_dist = d

        if min_dist > limit:
            clusters.append([])
            clusters[-1].append(chosen_vector)
        else:
            clusters[chosen_cluster].append(chosen_vector)
        data.remove(chosen_vector)

        # print(len(data))

    print(f"Time: {time.time() - start}")
    return clusters, None
