"""Logging helpers to keep instrumentation centralized."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
DEFAULT_LOG_PATH = LOG_DIR / "etl.log"


def configure_logging(log_path: Optional[Path] = None) -> None:
    """Configure root logger with a sane default format."""

    LOG_DIR.mkdir(exist_ok=True)
    log_file = log_path or DEFAULT_LOG_PATH

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
