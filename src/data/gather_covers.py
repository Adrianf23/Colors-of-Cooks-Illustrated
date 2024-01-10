from collections.abc import Iterable
from time import perf_counter
from typing import Any
import asyncio
import httpx
from dataclasses import dataclass, field

from selectolax.parser import HTMLParser
from urllib.parse import urljoin


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": "pl.String"})  # Polars metadata
    image_link: str | None = field(metadata={"dtype": "pl.String"})  # Polars metadata


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


def parse_cover_index_page(html: HTMLParser) -> Any:
    """
    parse_cover_index_page Generate an HTMLParser object to traverse for links

    parse_cover_index_page will return a generator object that is iterable object to save on memory. You will only get values out once you iterate through the return value.

    Args:
        html (HTMLParser): HTMLParser object that comes from the fetch_cover_html() method

    Yields:
        str: Generator object that can be iterated over
    """
    covers = html.css("li.indexable-book.listing")
    for cover in covers:
        yield urljoin(
            "https://www.eatyourbooks.com/", cover.css_first("a").attributes["href"]
        )


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


def extract_text(html: HTMLParser, sel: str):
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


async def fetch_all_cover_pages(
    client: httpx.AsyncClient, url: str, page_range: Iterable[int], **kwargs
):
    tasks = []
    for page_num in page_range:
        tasks.append(asyncio.create_task(fetch_cover_html(client, url, page=page_num)))
    results = await asyncio.gather(*tasks)
    return results


async def main():
    async with httpx.AsyncClient(http2=True) as client:
        magazine_cover_links = []
        magazine_desc = []

        page_range = range(
            13, 0, -1
        )  # 13 pages of results - set manually since you get 200 status even on out of bound pages
        cover_url = "https://www.eatyourbooks.com/magazines/cooks-illustrated/"

        start_time = perf_counter()

        top_level_cover_html = await fetch_all_cover_pages(
            client, cover_url, page_range
        )

        for page in top_level_cover_html:
            magazine_cover_links = parse_cover_index_page(page)
            for link in magazine_cover_links:
                print(link)
                individual_cover_html = await fetch_cover_html(client, link)
                magazine_desc.append(parse_individual_cover(individual_cover_html))

        print(magazine_desc)
        end_time = perf_counter()

        print(f"Total time to scrape: {(end_time - start_time):.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
