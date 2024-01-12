import polars as pl
import polars.selectors as cs
from polars.selectors import expand_selector
from pathlib import Path


magazine_path = Path(__file__).parents[2] / "data" / "raw" / "magazine_dump.parquet"


magazines = pl.scan_parquet(magazine_path)
