import asyncio
from dataclasses import dataclass, field

import gather_magazines as gm
import httpx
import polars as pl
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": pl.String})
    image_link: str | None = field(metadata={"dtype": pl.String})


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        base_url: str = "https://www.americastestkitchen.com/cooksillustrated/magazines"

        await page.goto(base_url)
        await asyncio.sleep(1)
        print("Visiting America's Test Kitchen")

        load_more_button = page.locator("button.Button-module_fill__UsoCz")

        while await load_more_button.count() > 0:
            await page.click("button.Button-module_fill__UsoCz")

        page_text: HTMLParser = HTMLParser(await page.content())
        await browser.close()

        results: list[Magazine] = []
        for item in gm.parse_item(page_text):
            results.append(item)

        dtype_dict: dict[str, str] = gm.gather_dtype(Magazine)
        magazine_covers: pl.DataFrame = pl.from_records(results, schema=dtype_dict)
        magazine_covers: pl.DataFrame = gm.clean_df_name(magazine_covers)
        magazine_covers.write_csv("./data/raw/magazine_covers.csv")

    async with httpx.AsyncClient(http2=True) as client:
        await gm.download_images(magazine_covers, client)


if __name__ == "__main__":
    asyncio.run(main())
