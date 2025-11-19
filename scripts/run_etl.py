"""CLI entrypoint for running the CORFO ETL pipeline."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.core.config import PipelineSettings
from src.core.logger import configure_logging
from src.etl.extract import CsvExtractor
from src.etl.load import CsvParquetLoader
from src.etl.transform import ProjectTransformer
from src.pipelines.etl_pipeline import EtlPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the CORFO ETL pipeline")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/settings.yaml"),
        help="Ruta al archivo YAML de configuración",
    )
    parser.add_argument(
        "--overrides",
        type=str,
        help="JSON string para sobreescribir valores del YAML",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Ruta opcional para el archivo de log",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    configure_logging(args.log_file)

    overrides: Dict[str, Any] = json.loads(args.overrides) if args.overrides else {}

    settings = PipelineSettings.from_yaml(args.config, overrides)
    extractor = CsvExtractor(settings.paths.raw_dataset, chunk_size=settings.etl.chunk_size)
    transformer = ProjectTransformer(settings.etl)
    loader = CsvParquetLoader(settings.processed_csv_path, settings.processed_parquet_path)

    pipeline = EtlPipeline(settings, extractor, transformer, loader)
    pipeline.run()


if __name__ == "__main__":  # pragma: no cover
    main()
