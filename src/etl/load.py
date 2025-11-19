"""Load layer persisting clean datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

import pandas as pd


class DataLoader(Protocol):
    """Generic interface for persisting dataframes."""

    def save(self, frame: pd.DataFrame) -> None:
        ...


class CsvParquetLoader(DataLoader):
    """Writes both CSV and Parquet outputs to keep analysts flexible."""

    def __init__(self, csv_path: Path, parquet_path: Path) -> None:
        self._csv_path = csv_path
        self._parquet_path = parquet_path

    def save(self, frame: pd.DataFrame) -> None:
        frame.to_csv(self._csv_path, index=False)
        frame.to_parquet(self._parquet_path, index=False)
