
from kmodes.kmodes import KModes
from sklearn.cluster import KMeans
from sklearn import preprocessing as sk_preprocessing


def kmeans_clustering(X_data, numClusters):
    kmeans = KMeans(n_clusters=numClusters, random_state=0).fit(X_data)
    return kmeans


def kmodes_clustering(X_data, numClusters):
    kmodes = KModes(n_clusters=numClusters).fit(X_data)
    return kmodes