import polars as pl
import numpy as np
from pathlib import Path
from PIL import Image


from sklearnex import patch_sklearn

patch_sklearn()

from sklearn.cluster import KMeans


def kmeans_img(*, filepath: str | Path, n_clusters: int) -> list[list[pl.Series]]:
    """
    kmeans_img Generate kmeans image classifier


    Args:
        `filepath` (str): Image filepath
        `n_clusters` (int): Number of centroids

    Returns:
        dict[pl.Series, pl.Series, pl.Series]: image, segmented image, and kmeans labels
    """
    with Image.open(filepath) as img:
        # Convert any RGBA -> RGB
        if np.asarray(img).shape[2] == 4:
            X = np.asarray(img.convert(mode="RGB")).reshape(-1, 3)
        else:
            X = np.asarray(img).reshape(-1, 3)
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(X)
        segmented_image = kmeans.cluster_centers_[kmeans.labels_].reshape(-1, 3)

    return [
        [pl.Series("filepath", filepath, dtype=pl.String)],
        [pl.Series("og_image", X, dtype=pl.List(pl.UInt8))],
        [pl.Series("segmented_image", segmented_image, dtype=pl.List(pl.UInt8))],
        [pl.Series("image_labels", kmeans.cluster_centers_, dtype=pl.List(pl.UInt8))],
    ]
