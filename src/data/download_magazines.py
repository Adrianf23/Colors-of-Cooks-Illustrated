from dataclasses import dataclass, field, fields
from pathlib import Path
import re
import httpx
from selectolax.parser import HTMLParser
from playwright.async_api import async_playwright
import polars as pl


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": pl.Utf8})
    image_link: str | None = field(metadata={"dtype": pl.Utf8})


def clean_link(
    text: str,
) -> str:
    """
    clean_link Extract text from a url, removing the text between two parantheses

    Args:
        text (str): String to replace

    Returns:
        str: Cleaned string
    """
    regex = r"\bupload\b(.+?)\/"  # this removes the text that is cropping the magazine covers in the browser
    replacement = "upload/"
    return re.sub(regex, replacement, text)


def parse_item(html_page: HTMLParser):
    data = html_page.css("picture.StandardCardImage_cardImage__pH9Yg")
    for item in data:
        yield (
            Magazine(
                name=item.css_first("img").attributes["alt"],
                image_link=item.css_first("img").attributes["src"],
            )
        )


def parse_dtype(self, attribute_name: str) -> dict[str, str]:
    """
    parse_dtype Parse the dtype metadata from a dataclass

    Args:
        attribute_name (str): Attribute in metadata of dataclass

    Returns:
        dict: Dictionary of metadata attribute and accompanying dtype
    """
    return {attribute_name: self.__dataclass_fields__[attribute_name].metadata["dtype"]}


def gather_dtype(dataclass_obj: Magazine) -> dict[str, str]:
    """
    gather_dtype Create a dictionary of dtypes from the dataclass metadata property

    Args:
        dataclass_obj (Magazine): Dataclass object of type Magazine

    Returns:
        dict[str, str]: Dictionary of {field: datatype} for each field in the Magazine dataclass
    """
    dtype_dict = {}
    field_names = [field.name for field in fields(dataclass_obj)]
    for field in field_names:
        dtype_dict.update(parse_dtype(dataclass_obj, field))
    return dtype_dict


def create_img_folder() -> Path:
    folder = input(str("Enter a folder to save your images: "))
    filepath = Path.cwd() / "data" / "raw" / folder
    Path.mkdir(filepath, exist_ok=True)
    print(f"Images will be saved here: {filepath}")
    return filepath


async def download_images(df: pl.DataFrame, client: httpx.AsyncClient) -> None:
    filepath = create_img_folder()

    for name, image_link in df.rows():
        filename = (filepath / name).with_suffix(".jpg")
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
