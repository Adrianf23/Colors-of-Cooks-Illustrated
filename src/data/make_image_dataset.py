import asyncio
from pathlib import Path
import httpx

import polars as pl

import download_covers as dc


async def main():
    async with httpx.AsyncClient(http2=True) as client:
        magazine_path = Path().cwd() / "data" / "raw" / "magazine_dump.parquet"
        magazines = pl.scan_parquet(magazine_path).collect()

        await dc.download_images(magazines, client)


if __name__ == "__main__":
    asyncio.run(main())
