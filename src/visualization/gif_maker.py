import glob
import shutil
from pathlib import Path
from re import split

import polars as pl
from PIL import Image, ImageSequence


def get_filtered_images() -> list[str]:
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
        for file in source:
            shutil.copy(file, f"{destination_path}/{Path(file).name}")
    else:
        for file in source.iterdir():
            if file.is_file():
                shutil.copy(
                    file,
                    f"{destination_path}/{split(r"-square", file.stem)[0]}{file.suffix}",
                )


def resize_image(image, size):
    return image.resize(size, Image.LANCZOS)


def combine_images(image_paths):
    images = [resize_image(Image.open(image), (1000, 1000)) for image in image_paths]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new("RGB", (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im


def make_gif(
    frame_folder: str | Path, output_file: Path, duration: int = 1000, loop: int = 0
):
    jpg_paths = glob.glob(f"{frame_folder}/*.jpg")
    webp_paths = glob.glob(f"{frame_folder}/*.webp")

    frames = []
    for i in range(0, min(len(jpg_paths), len(webp_paths)) - 1, 2):
        frames.append(combine_images([jpg_paths[i], webp_paths[i]]))

    frame_one: Image.Image = frames[0]
    frame_one.save(
        output_file,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=loop,
    )


def compress_gif(image: str | Path, output_file: Path):
    im: Image.Image = Image.open(image)

    output_width: int = int(im.width * 0.7)
    output_height: int = int(im.height * 0.7)

    frames = ImageSequence.Iterator(im)

    resized_frames = [
        frame.copy().resize((output_width, output_height), Image.LANCZOS)
        for frame in frames
    ]

    resized_frames[0].save(
        output_file,
        save_all=True,
        append_images=resized_frames[1:],
        loop=0,
        duration=im.info["duration"],
    )
