import asyncio
import httpx
import download_magazines as dm
import polars as pl
from dataclasses import dataclass, field
from playwright.async_api import async_playwright
from selectolax.parser import HTMLParser


@dataclass
class Magazine:
    name: str | None = field(metadata={"dtype": pl.String})
    image_link: str | None = field(metadata={"dtype": pl.String})


async def main():
    # Gather cover links
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        base_url = "https://www.americastestkitchen.com/cooksillustrated/magazines"

        await page.goto(base_url)
        await asyncio.sleep(0.1)
        print("Visiting America's Test Kitchen")

        load_more_button = page.locator("button.Button-module_fill__UsoCz")  # type: ignore

        while await load_more_button.count() > 0:
            await page.click("button.Button-module_fill__UsoCz")

        page_text = HTMLParser(await page.content())
        await browser.close()

        results = []
        for item in dm.parse_item(page_text):
            results.append(item)

        dtype_dict = dm.gather_dtype(Magazine)
        magazine_covers = pl.from_records(results, schema=dtype_dict)
        magazine_covers = dm.clean_df_name(magazine_covers)
        magazine_covers.write_csv("./data/raw/magazine_covers.csv")

    # Download cover links
    async with httpx.AsyncClient(http2=True) as client:
        await dm.download_images(magazine_covers, client)


if __name__ == "__main__":
    asyncio.run(main())
