from re import split
import polars as pl
from src.visualization.gif_maker import get_filtered_images
from src.visualization.gif_maker import make_gif
from src.visualization.gif_maker import transfer_files
from pathlib import Path


def main():
    og_image_list = get_filtered_images()
    destination_path = Path.cwd() / "data" / "processed" / "final-image-folder"
    Path.mkdir(destination_path, exist_ok=True)
    transfer_files(source=og_image_list, destination_path=destination_path)

    magazine_squares_filepath = Path.cwd() / "data" / "processed" / "kmeans-squares"
    transfer_files(source=magazine_squares_filepath, destination_path=destination_path)

    # make_gif(og_img_filepath)


if __name__ == "__main__":
    main()
