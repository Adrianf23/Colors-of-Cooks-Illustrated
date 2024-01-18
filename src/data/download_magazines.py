import httpx
import polars as pl
from dataclasses import dataclass, field, fields
from pathlib import Path
from selectolax.parser import HTMLParser
from typing import Any, Generator


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": pl.Utf8})
    image_link: str | None = field(metadata={"dtype": pl.Utf8})


def parse_item(html_page: HTMLParser) -> Generator[Magazine, Any, None]:
    """
    parse_item Take an HTMLParser object, return image and alt text

    Args:
        `html_page (HTMLParser)`: HTMLParser object from an HTTP request

    Yields:
        `Generator[Magazine, Any, None]`: Generator object of image and alt text
    """
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
        `attribute_name (str)`: Attribute in the metadata of a dataclass

    Returns:
        `dict[str, str]`: Dictionary of the metadata attribute and accompanying dtype from a dataclass
    """
    return {attribute_name: self.__dataclass_fields__[attribute_name].metadata["dtype"]}


def gather_dtype(dataclass_obj: Magazine) -> dict[str, str]:
    """
    gather_dtype Return a dictionary of fields and associated dtypes from a dataclass

    Args:
        `dataclass_obj (Magazine)`: Magazine dataclass

    Returns:
        `dict[str, str]`: Dictionary of {field: datatype} for each field in the Magazine dataclass
    """
    dtype_dict = {}
    field_names = [field.name for field in fields(dataclass_obj)]
    for field in field_names:
        dtype_dict.update(parse_dtype(dataclass_obj, field))
    return dtype_dict


# year code source: https://stackoverflow.com/a/77836528/8646265


# I chained a select statement after the with_column statement since I needed the year and months to create the filename. Source: https://stackoverflow.com/a/75601785/8646265
def clean_df_name(df: pl.DataFrame) -> pl.DataFrame:
    """
    clean_df_name Return a polars dataframe with some transformations applied

    Args:
        `df (pl.DataFrame)`: Polars DataFrame

    Returns:
        `pl.DataFrame`: Polars DataFrame
    """
    return df.with_columns(
        year=("1 " + pl.col("name").str.replace("/.* ", ""))
        .str.to_datetime("%d %B %Y")
        .dt.year(),
        start_month_num=("1 " + pl.col("name").str.replace("/.* ", ""))
        .str.to_datetime("%d %B %Y")
        .dt.month(),
        end_month_num=pl.col("name")
        .str.replace(".*/", "1 ")
        .str.to_datetime("%d %B %Y")
        .dt.month(),
        start_month_str=pl.col("name").str.extract(r"(\w+)\/"),
        end_month_str=pl.col("name").str.extract(r"\/(\w+)"),
        cleaned_link=pl.col("image_link").str.replace(r"\bupload\b(.+?)\/", "upload/"),
        # Some of the magazines are blank and all have the same link
        is_blank_cover=pl.when(
            pl.col("image_link").str.contains(
                r"https://res.cloudinary.com/hksqkdlah/image/upload/Recipe_Default_zbu7tq"
            )
        )
        .then(pl.lit(1, dtype=pl.Int8))
        .otherwise(pl.lit(0, dtype=pl.Int8)),
    ).select(
        pl.col("*").exclude("image_link"),
        filename=pl.concat_str(
            [
                pl.col("year"),
                pl.col("start_month_num"),
                pl.col("end_month_num"),
            ],
            separator="_",
        ),
    )


def create_img_folder() -> Path:
    """
    create_img_folder Return a pathlib object from user input

    Returns:
        `Path`: Pathlib object
    """
    folder = input(str("Enter a folder to save your images: "))
    filepath = Path.cwd() / "data" / "raw" / folder
    Path.mkdir(filepath, parents=True, exist_ok=True)
    print(f"Images will be saved here: {filepath}")
    return filepath


async def download_images(df: pl.DataFrame, client: httpx.AsyncClient) -> None:
    """
    download_images Return a list of images to the specified folder in `create_img_folder`

    Args:
        `df (pl.DataFrame)`: Polars DataFrame
        `client (httpx.AsyncClient)`: HTTPx AsyncClient
    """
    filepath = create_img_folder()

    # Inefficient implentation. TODO: Find columnar implementation
    for row in df.iter_rows(named=True):
        filename = (filepath / row["filename"]).with_suffix(".jpg")
        async with client.stream("GET", row["cleaned_link"]) as response:
            print("Downloading the images...")
            with open(filename, "wb") as f:
                print("Writing data to file")
                async for chunk in response.aiter_bytes(
                    chunk_size=4096
                ):  # abritrary chunk size
                    f.write(chunk)
        print(f"File saved as {filename}")

    print("Download complete")
