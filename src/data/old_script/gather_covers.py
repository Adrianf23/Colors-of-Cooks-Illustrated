import asyncio
import httpx
import polars as pl
from collections.abc import Iterable
from dataclasses import dataclass, field, fields
from selectolax.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": pl.Utf8})
    image_link: str | None = field(metadata={"dtype": pl.Utf8})


async def fetch_cover_html(client: httpx.AsyncClient, url: str, **kwargs) -> Any:
    """
    fetch_cover_html Gathers the HTML Node from a specific page

    Args:
        client (httpx.AsyncClient): Httpx async client for accessing the website efficiently
        url (str): Url to query
        **kwargs: Additional arguments such as page number. Skipped on the first page to allow for redirects

    Returns:
        Any: HTMLParser object that can be accessed in with the `extract_text` function
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    if kwargs.get("page"):
        resp = await client.get(
            url=urljoin(url, str(kwargs.get("page"))),
            headers=headers,
            follow_redirects=True,
        )

    else:
        resp = await client.get(url=url, headers=headers, follow_redirects=True)

    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. Page limit exceeded"
        )
        return False

    html = HTMLParser(html=resp.text)
    return html


async def fetch_all_cover_pages(
    client: httpx.AsyncClient, url: str, page_range: Iterable[int], **kwargs
) -> list[HTMLParser]:
    """
    fetch_all_cover_pages Async client that returns a list of HTMLParser objects

    Takes in an async client, url and page range to asynchronously return a list of HTMLParse objects corresping to each page

    Args:
        client (httpx.AsyncClient): Async client from the httpx library
        url (str): url to parse
        page_range (Iterable[int]): list of page numbers to loop through

    Returns:
        _type_: _description_
    """
    tasks = []
    for page_num in page_range:
        tasks.append(asyncio.create_task(fetch_cover_html(client, url, page=page_num)))
    results = await asyncio.gather(*tasks)
    return results


page_range = range(
    13, 0, -1
)  # 13 pages of results - set manually since you get 200 status even on out of bound pages.


def parse_cover_index_page(url: str, html: HTMLParser) -> Any:
    """
    parse_cover_index_page Generate an HTMLParser object to traverse for links

    Return a generator object that is iterable object to save on memory.

    Args:
        url (str): URL to parse
        html (HTMLParser): HTMLParser object that comes from the fetch_cover_html() method

    Yields:
        str: Generator object of url hrefs
    """
    covers = html.css("li.indexable-book.listing")
    for cover in covers:
        yield urljoin(url, cover.css_first("a").attributes["href"])


def parse_individual_cover(html: HTMLParser) -> Magazine:
    """
    parse_individual_cover Method for accessing individual magazine names

    This method creates a new Magazine dataclass for each url that includes the name and a link to the image for later processing

    Args:
        html (HTMLParser): HTMLParser object that comes from the fetch_cover_html() method

    Returns:
        Magazine: Magazine dataclass that inclues "name" and "image_link" as attributes
    """
    new_cover = Magazine(
        name=extract_text(html, "h1"),
        image_link=html.css_first("img.img-maxwidth").attributes["src"],
    )
    return new_cover


def clean_up_data(value: str) -> str:
    return value.strip()


def extract_text(html: HTMLParser, sel: str) -> str | None:
    """
    extract_text Extract css selector from the page

    Args:
        html (HTMLParser): HTMLParser object gathered from a previous async call
        sel (str): CSS selector from the selectolax package

    Returns:
        str | None: text from the page that matches the CSS selector. If it's not found, return None.
    """
    try:
        text = html.css_first(sel).text()
        return clean_up_data(text)
    except AttributeError:
        return None


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
