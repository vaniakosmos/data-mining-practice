import random

from lab4.utils import dist


def k_nearest_neighbours(data: list, k, c=2):

    # clusters = [[(-1, 0)], [(1, 0)]]
    clusters = [[data[random.randint(0, len(data))]] for _ in range(k)]

    while len(data) > 0:
        temp_cluster = [[] for _ in range(k)]

        for vector1 in data:
            chosen_cluster, min_dist = None, None
            for cluster_id, cluster in enumerate(clusters):
                for vector2 in cluster[-c:]:
                    d = dist(vector1, vector2)
                    if min_dist is None or d < min_dist:
                        chosen_cluster = cluster_id
                        min_dist = d
            temp_cluster[chosen_cluster].append((vector1, min_dist))

        added = []

        for index, cluster in enumerate(temp_cluster):
            cluster.sort(key=lambda x: x[1])
            add = [e[0] for e in cluster[:c]]
            added.extend(add)
            clusters[index].extend(add)

        for vec in added:
            data.remove(vec)

        print(len(data))

    return clusters, None
