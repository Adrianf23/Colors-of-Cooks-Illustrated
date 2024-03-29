from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image
from sklearnex import patch_sklearn

patch_sklearn()  # Comment out if you don't want to use this

from sklearn.cluster import KMeans  # noqa: E402


def kmeans_img(filepath: str | Path, n_clusters: int) -> tuple[np.ndarray, np.ndarray]:
    """
    kmeans_img Generate kmeans image classifier


    Args:
        `filepath` (str): Image filepath
        `n_clusters` (int): Number of centroids

    Returns:
        tuple[np.ndarray, np.ndarray]: centroids and image labels
    """

    with Image.open(filepath) as img:
        # Convert any RGBA -> RGB
        if np.asarray(img).shape[2] == 4:
            X: np.ndarray = np.asarray(img.convert(mode="RGB")).reshape(-1, 3)
        else:
            X = np.asarray(img).reshape(-1, 3)
        kmeans: KMeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(X)
        color_palette = kmeans.cluster_centers_
        color_labels = kmeans.labels_

    return color_palette, color_labels


def get_color_labels(color_labels: np.ndarray) -> list[tuple]:
    """
    get_color_labels Extract 4 colors from KMeans labels

    Args:
        color_labels (np.ndarray): labels from kmeans_img function

    Returns:
        list[tuple]: list of RGB values for each of the 4 colors
    """

    color_indices: list[int] = [1, 0, 2, 6]
    color_counter: list[tuple] = Counter(color_labels).most_common(10)

    color_square_list: list[tuple] = [color_counter[i][0] for i in color_indices]
    return color_square_list
