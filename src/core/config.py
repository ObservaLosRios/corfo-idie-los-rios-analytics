"""Configuration helpers for the ETL pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, field_validator

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class BooleanMapping(BaseModel):
    """Explicit text to boolean conversion references."""

    affirmative: List[str] = Field(default_factory=list)
    negative: List[str] = Field(default_factory=list)

    @field_validator("affirmative", "negative", mode="before")
    @classmethod
    def _normalize_entries(cls, values: List[str]) -> List[str]:
        return [value.strip().lower() for value in values]


class EtlSettings(BaseModel):
    chunk_size: int = 1000
    currency_columns: List[str] = Field(default_factory=list)
    date_columns: List[str] = Field(default_factory=list)
    boolean_mappings: BooleanMapping = Field(default_factory=BooleanMapping)


class PathSettings(BaseModel):
    raw_dataset: Path
    processed_dir: Path
    interim_dir: Path

    @field_validator("raw_dataset", "processed_dir", "interim_dir", mode="before")
    @classmethod
    def _resolve_relative(cls, value: str) -> Path:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path


class OutputSettings(BaseModel):
    csv_name: str = "corfo_projects.csv"
    parquet_name: str = "corfo_projects.parquet"


class PipelineSettings(BaseModel):
    paths: PathSettings
    output: OutputSettings
    etl: EtlSettings

    @classmethod
    def from_yaml(cls, config_path: Path, overrides: Optional[Dict[str, Any]] = None) -> "PipelineSettings":
        data = cls._read_yaml(config_path)
        if overrides:
            data = cls._deep_merge(data, overrides)
        return cls(**data)

    @staticmethod
    def _read_yaml(config_path: Path) -> Dict[str, Any]:
        with config_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)

    @staticmethod
    def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        merged: Dict[str, Any] = dict(base)
        for key, value in override.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = PipelineSettings._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    @property
    def processed_csv_path(self) -> Path:
        return self.paths.processed_dir / self.output.csv_name

    @property
    def processed_parquet_path(self) -> Path:
        return self.paths.processed_dir / self.output.parquet_name

    def ensure_output_dirs(self) -> None:
        self.paths.processed_dir.mkdir(parents=True, exist_ok=True)
        self.paths.interim_dir.mkdir(parents=True, exist_ok=True)
