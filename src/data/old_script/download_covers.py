from functools import reduce
from pathlib import Path

import polars as pl

import httpx

from typing import Any


def create_img_folder() -> Path:
    folder = input(str("Enter a folder to save your images: "))
    filepath = Path.cwd() / "data" / "raw" / folder
    Path.mkdir(filepath, exist_ok=True)
    print(f"Images will be saved here: {filepath}")
    return filepath


replacement_dict = {
    "\n": "",
    "  ": "",
    ": ": "_",
    " ": "-",
    ",": "",
    "/": "_",
    "'": "",
    "\u2019": "",
    "\u00a0": "-",
    "(": "",
    ")": "",
    ",": "",
    "&": "and",
    "by": "-by",
}


# Reduce code from: https://stackoverflow.com/a/71234570/8646265
def clean_file(
    string_to_replace: str, replacement_dict: dict[str, str] = replacement_dict
) -> str:
    cleaned_string = reduce(
        lambda x, y: x.replace(*y), [string_to_replace, *list(replacement_dict.items())]
    )
    return cleaned_string


async def download_images(df: pl.DataFrame, client: httpx.AsyncClient) -> None:
    filepath = create_img_folder()

    for name, image_link in df.rows():
        filename = (filepath / clean_file(name)).with_suffix(".jpg")
        async with client.stream("GET", image_link) as response:
            print("Downloading the images...")
            with open(filename, "wb") as f:
                print("Writing data to file")
                async for chunk in response.aiter_bytes(
                    chunk_size=4096
                ):  # abritrary chunk size
                    f.write(chunk)
        print(f"File saved as {filename}")

    print("Download complete")
