from collections import Counter
import numpy as np
from pathlib import Path
from PIL import Image


from sklearnex import patch_sklearn

patch_sklearn()

from sklearn.cluster import KMeans


def kmeans_img(
    *, filepath: str | Path, n_clusters: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    kmeans_img Generate kmeans image classifier


    Args:
        `filepath` (str): Image filepath
        `n_clusters` (int): Number of centroids

    Returns:
        list[list[pl.Series]]: filepath, image, segmented image, and kmeans labels
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
    color_indices: list[int] = [1, 0, 2, 9]
    color_counter: list[tuple] = Counter(color_labels).most_common(10)

    color_square_list: list[tuple] = [color_counter[i][0] for i in color_indices]
    return color_square_list
