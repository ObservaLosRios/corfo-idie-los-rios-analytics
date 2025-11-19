"""Extraction layer for reading CORFO datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional, Protocol

import pandas as pd


class DataExtractor(Protocol):
    """Simple iterator interface returning DataFrame chunks."""

    def read(self) -> Iterator[pd.DataFrame]:
        ...


class CsvExtractor(DataExtractor):
    """Chunked CSV reader to minimize memory pressure."""

    def __init__(
        self,
        csv_path: Path,
        chunk_size: int,
        encoding: str = "utf-8",
        na_values: Optional[list[str]] = None,
    ) -> None:
        self._csv_path = csv_path
        self._chunk_size = chunk_size
        self._encoding = encoding
        self._na_values = na_values or ["", "NA", "N/A", "null", "NULL"]

    def read(self) -> Iterator[pd.DataFrame]:
        reader = pd.read_csv(
            self._csv_path,
            chunksize=self._chunk_size,
            dtype=str,
            encoding=self._encoding,
            na_values=self._na_values,
            keep_default_na=True,
        )
        for chunk in reader:
            yield chunk
