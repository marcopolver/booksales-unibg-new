import numpy as np
from copy import deepcopy

'''
Function that returns k clusters from the given data X
'''
def calculate_clusters(X, k):

    n = X.shape[0]
    c = X.shape[1]

    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    centers = np.random.randn(k, c) * std + mean

    centers_old = np.zeros(centers.shape)
    centers_new = deepcopy(centers)
    clusters = np.zeros(n)
    distances = np.zeros((n, k))
    error = np.linalg.norm(centers_new - centers_old)

    while error != 0:
        for i in range(k):
            distances[:, i] = np.linalg.norm(X - centers_new[i], axis=1)
        clusters = np.argmin(distances, axis=1)
        centers_old = deepcopy(centers_new)
        for i in range(k):
            centers_new[i] = np.nanmean(X[clusters == i], axis=0)

        error = np.linalg.norm(centers_new - centers_old)

    #plt.scatter(X[:, 0], X[:, 1], s=25, c=clusters, cmap='viridis')
    #plt.scatter(centers_new[:, 0], centers_new[:, 1], marker='*', c='g', s=150)
    #plt.show()

    return clusters, centers_new

def cluster_cost(X, cluster_number, clusters, center):

    points = list()
    for i in range(len(X)):
        if clusters[i] == cluster_number:
            points.append(X[i])

    n = len(points)
    value = 0

    for point in points:

        value += abs(np.linalg.norm(point - center))

    return value/n

def total_cost(clusters_costs):
    return sum(clusters_costs)/len(clusters_costs)

def elbow_kmeans(X, max_k):

    derivata = -100000
    t_cost_new = 1000
    t_cost_old = 1000
    k = 2
    clusters = None
    centers = None

    while abs(derivata)>0.1 and k<=max_k:

        t_cost_old = t_cost_new

        clusters, centers = calculate_clusters(X, k)

        numbers = list(set(clusters))

        list_costs = list()

        for i in range(len(numbers)):
            cost = cluster_cost(X, numbers[i], clusters, centers[i])
            list_costs.append(cost)

        t_cost_new = total_cost(list_costs)

        derivata = t_cost_new-t_cost_old

        print(k)
        k = k + 1

        print(derivata)

    return clusters, centers, k
