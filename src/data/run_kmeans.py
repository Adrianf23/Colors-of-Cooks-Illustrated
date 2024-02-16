import polars as pl
from kmeans import kmeans_img
from pathlib import Path, PurePath
from time import perf_counter


def main():
    image_filepath: Path = Path.cwd() / "data" / "raw" / "cooks-illustrated"
    files: list[str] = [
        str(path) for path in image_filepath.rglob("*") if path.is_file()
    ]

    kmean_folder: str = input(
        str("Name the folder where the KMeans data will be stored: ")
    )
    parquet_filepath: Path = Path.cwd() / "data" / "interim" / kmean_folder
    Path.mkdir(parquet_filepath, exist_ok=True)
    print(f"KMeans data will be saved here: {parquet_filepath}")

    start: float = perf_counter()

    for file in files:
        file_header = PurePath(file).stem
        if Path(f"{parquet_filepath} / {file_header}_cover.parquet").exists() == True:
            continue
        else:
            print(f"New file: {file}")
            print("Exporting to parquet")
            print("....................")
            pl.from_records(
                kmeans_img(filepath=file, n_clusters=10),
                schema=[
                    "filepath",
                    "filename",
                    "og_image",
                    "segmented_image",
                    "image_labels",
                ],
            ).write_parquet(
                file=f"{parquet_filepath}/{file_header}_cover.parquet",
                compression="zstd",
                compression_level=22,
                use_pyarrow=True,
            )
            print("....................")
    end: float = perf_counter()
    print("Finished exporting all files")
    print(f"End of script. Took {end-start} seconds.")


if __name__ == "__main__":
    main()
