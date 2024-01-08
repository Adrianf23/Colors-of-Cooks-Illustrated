from typing import Any
import asyncio
import httpx
from dataclasses import dataclass

from selectolax.parser import HTMLParser
from urllib.parse import urljoin


@dataclass
class Magazine:
    name: str | None
    month: str | None
    year: int | None
    image: str | None


async def fetch_cover_html(client: httpx.AsyncClient, url: str, **kwargs) -> Any:
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


async def main():
    # record the starting time
    # start = time.perf_counter()

    async with httpx.AsyncClient(http2=True) as client:
        tasks = []
        cover_url = "https://www.eatyourbooks.com/magazines/cooks-illustrated/"
        for i in range(1, 14):
            tasks.append(
                asyncio.create_task(
                    fetch_cover_html(client=client, url=cover_url, page=i)
                )
            )
        results = await asyncio.gather(*tasks)

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
