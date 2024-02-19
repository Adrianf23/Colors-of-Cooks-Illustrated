import glob
import polars as pl
import shutil
from pathlib import Path
from PIL import Image
from re import split

def make_gif(frame_folder, duration=500, loop=0):
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.webp")]
    frame_one = frames[0]
    frame_one.save(
        "output.gif",
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=loop,
    )


def get_filtered_images():
    og_img_filepath: Path = Path.cwd() / "data" / "raw" / "cooks-illustrated"
    files: list[tuple[str, str]] = [
        (str(path), path.stem) for path in og_img_filepath.rglob("*") if path.is_file()
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

    return filtered_files


def transfer_files(source: list[str] | Path, destination_path: str | Path):
    source = source
    destination_path = destination_path

    if isinstance(source, list):
        for file in source:  # type: ignore
            shutil.copy(file, f"{destination_path}/{Path(file).name}")  # type: ignore
    else:
        for file in source.iterdir():
            if file.is_file():
                shutil.copy(file, f"{destination_path}/{split(r"-square", file.stem)[0]}{file.suffix}")
