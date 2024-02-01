from kmeans import kmeans_img
import polars as pl
from pathlib import Path
from time import perf_counter



def main():
    image_filepath = Path.cwd() / "data" / "raw" / "cooks-illustrated"
    files = [str(path) for path in image_filepath.rglob("*") if path.is_file()]

    start = perf_counter()
    parquet_filepath = Path.cwd() / "data" / "interim"

    for i, v in enumerate(files):
        if Path(f"{parquet_filepath / v.split("\\")[-1].strip(".jpg")}_cover.parquet").exists() == True:
            continue
        else:
            print(f"New file: {v}")
            print("Exporting to parquet")
            print("....................")
            pl.from_records(
                kmeans_img(filepath=files[i], n_clusters=2), schema=["filepath", "og_image", "segmented_image", "image_labels"]
            ).write_parquet(
                file=f"{parquet_filepath/v.split("\\")[-1].strip(".jpg")}_cover.parquet", compression="zstd", compression_level=20, use_pyarrow=True
            )
            print("....................")
    end = perf_counter()
    print("Finished exporting all files")
    print(f"End of script. Took {end-start} seconds.")

if __name__ == "__main__":
    main()
