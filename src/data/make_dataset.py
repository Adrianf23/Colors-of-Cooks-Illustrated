import asyncio
from dataclasses import dataclass, field
from time import perf_counter

import httpx
import gather_covers

import polars as pl


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": pl.Utf8})
    image_link: str | None = field(metadata={"dtype": pl.Utf8})


async def main():
    async with httpx.AsyncClient(http2=True) as client:
        magazine_cover_links = []
        magazine_desc = []

        page_range = gather_covers.page_range

        cover_url = "https://www.eatyourbooks.com/magazines/cooks-illustrated/"
        cover_url_stem = "https://www.eatyourbooks.com/"

        start_time = perf_counter()

        top_level_cover_html = await gather_covers.fetch_all_cover_pages(
            client, cover_url, page_range
        )

        for page in top_level_cover_html:
            magazine_cover_links = gather_covers.parse_cover_index_page(
                cover_url_stem, page
            )
            for link in magazine_cover_links:
                print(f"Retrieving {link}")
                individual_cover_html = await gather_covers.fetch_cover_html(
                    client, link
                )
                magazine_desc.append(
                    gather_covers.parse_individual_cover(individual_cover_html)
                )
                await asyncio.sleep(
                    1
                )  # rip to performance, but this is needed so you aren't rate limited

        end_time = perf_counter()

        print(f"Total time to scrape: {(end_time - start_time):.2f} seconds")

        dtype_dict = gather_covers.gather_dtype(Magazine)  # type: ignore
        df = pl.from_records(magazine_desc, schema=dtype_dict)  # type: ignore
        print(df)
        df.write_parquet("./data/raw/magazine_dump.parquet")
        df.write_csv(
            "./data/raw/magazine_dump.csv"
        )  # comparing file size - 10x savings


if __name__ == "__main__":
    asyncio.run(main())
