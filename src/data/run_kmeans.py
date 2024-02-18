import polars as pl
from kmeans import kmeans_img
from pathlib import Path, PurePath
from time import perf_counter


def main():
    image_filepath: Path = Path.cwd() / "data" / "raw" / "cooks-illustrated"
    files: list[str] = [
        str(path) for path in image_filepath.rglob("*") if path.is_file()
    ]

    # TODO: Load in the magazine_cover.csv and filter for the nonblank images
    # TODO: Filter the `files` list to only return the images we will be using

    kmean_folder: str = input(
        str("Name the folder where the KMeans data will be stored: ")
    )
    csv_filepath: Path = Path.cwd() / "data" / "interim" / kmean_folder
    Path.mkdir(csv_filepath, exist_ok=True)
    print(f"KMeans data will be saved here: {csv_filepath}")

    start: float = perf_counter()

    for file in files:
        file_header: str = PurePath(file).stem
        # TODO: Run kmeans function here and just save the segmented image
        segmented_image = kmeans_img(filepath=file, n_clusters=10)

        # TODO: Run logic for saving the top 10 images
    end: float = perf_counter()
    print("Finished exporting all files")
    print(f"End of script. Took {end-start} seconds.")


if __name__ == "__main__":
    main()
