from typing import Any
import polars as pl
import numpy as np
from pathlib import Path, PurePath
from PIL import Image


from sklearnex import patch_sklearn

patch_sklearn()

from sklearn.cluster import KMeans


def kmeans_img(
    *, filepath: str | Path, n_clusters: int
) -> tuple[np.ndarray, list[list[str | Path] | list[str]]]:
    """
    kmeans_img Generate kmeans image classifier


    Args:
        `filepath` (str): Image filepath
        `n_clusters` (int): Number of centroids

    Returns:
        list[list[pl.Series]]: filepath, image, segmented image, and kmeans labels
    """
    file_stem: str = PurePath(filepath).stem

    with Image.open(filepath) as img:
        # Convert any RGBA -> RGB
        if np.asarray(img).shape[2] == 4:
            X: np.ndarray = np.asarray(img.convert(mode="RGB")).reshape(-1, 3)
        else:
            X = np.asarray(img).reshape(-1, 3)
        kmeans: KMeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(X)
        segmented_image: np.ndarray = kmeans.cluster_centers_[kmeans.labels_].reshape(
            -1, 3
        )

    return segmented_image, [
        [filepath],
        [file_stem],
    ]
