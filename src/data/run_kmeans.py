from pathlib import Path

import kmeans as km
import matplotlib.pyplot as plt
import polars as pl
from PIL import Image, ImageDraw


def main():
    image_filepath: Path = Path.cwd() / "data" / "raw" / "cooks-illustrated"

    # tuple of (filepath and file stem) - filepath is for kmeans and file stem is for filtering on the below magazine dataframe
    files: list[tuple[str, str]] = [
        (str(path), path.stem) for path in image_filepath.rglob("*") if path.is_file()
    ]

    magazine_filepath: Path = Path.cwd() / "data" / "raw" / "magazine_covers.csv"
    magazine_covers: pl.DataFrame = (
        pl.read_csv(magazine_filepath)
        .filter(pl.col.is_blank_cover != 1)
        .select(pl.exclude("is_blank_cover"))
    )

    filtered_magazines: list[str] = magazine_covers.get_column("filename").to_list()
    filtered_files: list[str] = [
        file[0] for file in files if file[1] in filtered_magazines
    ]

    kmeans_folder: str = input(
        str("Name the folder where the KMeans color squares will be stored: ")
    )
    color_square_filepath: Path = Path.cwd() / "data" / "processed" / kmeans_folder
    Path.mkdir(color_square_filepath, exist_ok=True)
    print(f"Segmented images will be saved here: {color_square_filepath}")

    for file in filtered_files:
        if (
            Path(f"{color_square_filepath}/{Path(file).stem}-square.webp").exists()
            is True
        ):
            continue
        else:
            color_palette, color_labels = km.kmeans_img(filepath=file, n_clusters=10)

            color_square_list: list = km.get_color_labels(color_labels)

            image: Image.Image = Image.new("RGB", (200, 200), "white")
            draw = ImageDraw.Draw(image)

            # Define the coordinates for the big square
            big_square_coords: tuple[int, int, int, int] = (0, 0, 200, 200)

            # Define the coordinates for the three inner squares
            inner_square1_coords: tuple[int, int, int, int] = (25, 25, 100, 175)
            inner_square2_coords: tuple[int, int, int, int] = (100, 25, 175, 100)
            inner_square3_coords: tuple[int, int, int, int] = (100, 100, 175, 175)

            # Draw the big square
            draw.rectangle(
                big_square_coords,
                fill=tuple(color_palette[color_square_list[0]].astype(int)),
            )

            # Draw the three inner squares
            draw.rectangle(
                inner_square1_coords,
                fill=tuple(color_palette[color_square_list[1]].astype(int)),
            )
            draw.rectangle(
                inner_square2_coords,
                fill=tuple(color_palette[color_square_list[2]].astype(int)),
            )
            draw.rectangle(
                inner_square3_coords,
                fill=tuple(color_palette[color_square_list[3]].astype(int)),
            )

            # Display the image
            plt.imshow(image)
            plt.axis("off")

            plt.savefig(
                f"{color_square_filepath}/{Path(file).stem}-square.webp",
                bbox_inches="tight",
                pad_inches=0,
                dpi=300,
            )
    print("Finished exporting all files")


if __name__ == "__main__":
    main()
