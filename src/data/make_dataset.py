import asyncio
from dataclasses import dataclass, field, fields
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
        dtype_dict = {}
        field_names = [field.name for field in fields(Magazine)]

        for field in field_names:
            dtype_dict.update(gather_covers.parse_dtype(Magazine, field))

        magazine_cover_links = []
        magazine_desc = []

        page_range = range(
            13, 0, -1
        )  # 13 pages of results - set manually since you get 200 status even on out of bound pages.

        cover_url = "https://www.eatyourbooks.com/magazines/cooks-illustrated/"

        start_time = perf_counter()

        top_level_cover_html = await gather_covers.fetch_all_cover_pages(
            client, cover_url, page_range
        )

        for page in top_level_cover_html:
            magazine_cover_links = gather_covers.parse_cover_index_page(page)
            for link in magazine_cover_links:
                print(link)
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

        df = pl.from_records(magazine_desc, schema=dtype_dict)
        print(df)
        df.write_parquet("./data/raw/magazine_dump.parquet")
        df.write_csv(
            "./data/raw/magazine_dump.csv"
        )  # comparing file size - 10x savings


if __name__ == "__main__":
    asyncio.run(main())
