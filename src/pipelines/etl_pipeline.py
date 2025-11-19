"""Orchestrators that compose the ETL flow."""

from __future__ import annotations

import logging
from typing import Iterable

import pandas as pd

from src.core.config import PipelineSettings
from src.etl.extract import DataExtractor
from src.etl.load import DataLoader
from src.etl.transform import DataTransformer

_LOGGER = logging.getLogger(__name__)


class EtlPipeline:
    """Coordinates extract-transform-load dependencies."""

    def __init__(
        self,
        settings: PipelineSettings,
        extractor: DataExtractor,
        transformer: DataTransformer,
        loader: DataLoader,
    ) -> None:
        self._settings = settings
        self._extractor = extractor
        self._transformer = transformer
        self._loader = loader

    def run(self) -> pd.DataFrame:
        self._settings.ensure_output_dirs()
        frames: list[pd.DataFrame] = []
        total_rows = 0

        for chunk in self._extractor.read():
            transformed = self._transformer.transform(chunk)
            frames.append(transformed)
            total_rows += len(transformed)

        if not frames:
            raise ValueError("Extractor produced zero chunks; aborting load.")

        final_frame = pd.concat(frames, ignore_index=True)
        self._loader.save(final_frame)
        _LOGGER.info("ETL completed: %s rows.", total_rows)
        return final_frame
