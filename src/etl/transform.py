"""Transformation layer converting raw CSV chunks into clean tables."""

from __future__ import annotations

import logging
from typing import Iterable, Protocol

import pandas as pd

from src.core.config import EtlSettings

_LOGGER = logging.getLogger(__name__)


class DataTransformer(Protocol):
    """Callable transforming DataFrame chunks."""

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        ...


class ProjectTransformer(DataTransformer):
    """Domain-specific transformer encapsulating business rules."""

    def __init__(self, settings: EtlSettings) -> None:
        self._settings = settings

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        current = frame.copy()
        current = self._standardize_columns(current)
        current = self._clean_currency_fields(current)
        current = self._normalize_boolean_fields(current)
        current = self._parse_dates(current)
        return current

    def _standardize_columns(self, frame: pd.DataFrame) -> pd.DataFrame:
        return frame.apply(lambda col: col.map(self._clean_text))

    @staticmethod
    def _clean_text(value: object) -> object:
        if isinstance(value, str):
            return " ".join(value.strip().split())
        return value

    def _clean_currency_fields(self, frame: pd.DataFrame) -> pd.DataFrame:
        for column in self._settings.currency_columns:
            if column not in frame:
                _LOGGER.warning("Currency column %s missing in chunk", column)
                continue
            frame[column] = (
                frame[column]
                .astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            frame[column] = frame[column].replace("nan", pd.NA)
            frame[column] = frame[column].astype("Int64")
        return frame

    def _normalize_boolean_fields(self, frame: pd.DataFrame) -> pd.DataFrame:
        affirmative = set(value.lower() for value in self._settings.boolean_mappings.affirmative)
        negative = set(value.lower() for value in self._settings.boolean_mappings.negative)

        bool_columns = self._infer_boolean_columns(frame.columns)
        for column in bool_columns:
            series = frame[column]
            normalized = series.astype(str).str.lower().str.strip()
            bool_series = pd.Series(pd.NA, index=series.index, dtype="boolean")
            bool_series = bool_series.mask(normalized.isin(affirmative), True)
            bool_series = bool_series.mask(normalized.isin(negative), False)
            frame[column] = bool_series
        return frame

    @staticmethod
    def _infer_boolean_columns(columns: Iterable[str]) -> list[str]:
        tokens = {"mujer", "sostenible", "economía circular", "ley rep", "criterio"}
        return [col for col in columns if any(token in col.lower() for token in tokens)]

    def _parse_dates(self, frame: pd.DataFrame) -> pd.DataFrame:
        for column in self._settings.date_columns:
            if column not in frame:
                _LOGGER.warning("Date column %s missing in chunk", column)
                continue
            parsed = pd.to_datetime(frame[column], errors="coerce", utc=False)
            frame[column] = parsed
        return frame
