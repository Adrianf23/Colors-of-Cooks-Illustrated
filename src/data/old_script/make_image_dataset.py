import asyncio
import httpx
import download_covers as dc
import polars as pl
from pathlib import Path


async def main():
    async with httpx.AsyncClient(http2=True) as client:
        magazine_path = Path().cwd() / "data" / "raw" / "magazine_dump.parquet"
        magazines = pl.scan_parquet(magazine_path).collect()

        await dc.download_images(magazines, client)


if __name__ == "__main__":
    asyncio.run(main())
