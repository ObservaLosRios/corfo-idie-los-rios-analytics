"""Reusable helpers for Región de Los Ríos visualizations."""

from __future__ import annotations

import unicodedata
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
import plotly.express as px

TARGET_REGION = "Region De Los Rios"
PALETTE = {
    "los_rios": "#E4572E",
    "otras": "#9CA3AF",
}
SECONDARY_COLOR = "#1D4ED8"
CURRENCY_COLUMNS = [
    "Financiamiento Innova",
    "Aprobado Privado",
    "Aprobado Privado Pecuniario",
    "Monto Certificado Ley",
]
DEFAULT_COLOR_SEQUENCE = px.colors.qualitative.G10


__all__ = [
    "TARGET_REGION",
    "PALETTE",
    "SECONDARY_COLOR",
    "CURRENCY_COLUMNS",
    "DEFAULT_COLOR_SEQUENCE",
    "load_dataset",
    "build_region_summary",
    "select_top_regions",
    "build_region_color_map",
    "build_yearly_region_projects",
    "build_panel_finance",
]


def normalize_region(name: str | float) -> str | float:
    if pd.isna(name):
        return name
    ascii_name = (
        unicodedata.normalize("NFKD", str(name))
        .encode("ascii", "ignore")
        .decode("utf-8")
    )
    return ascii_name.strip().title()


def coerce_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"No se encontró {path}. Ejecuta el ETL antes de continuar."
        )

    frame = pd.read_csv(path)
    frame.columns = [col.strip() for col in frame.columns]
    frame["Region_Normalizada"] = frame["Región"].map(normalize_region)

    for column in CURRENCY_COLUMNS:
        if column in frame:
            frame[column] = coerce_numeric(frame[column])

    frame["Año Adjudicación"] = pd.to_numeric(frame["Año Adjudicación"], errors="coerce")
    frame["anio_dt"] = pd.to_datetime(
        frame["Año Adjudicación"].astype("Int64"), format="%Y", errors="coerce"
    )
    frame["es_los_rios"] = frame["Region_Normalizada"].eq(TARGET_REGION)
    return frame


def build_region_summary(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby("Region_Normalizada")
        .agg(
            total_innova=("Financiamiento Innova", "sum"),
            proyectos=("Código Proyecto", "count"),
            promedio_privado=("Aprobado Privado", "mean"),
        )
        .reset_index()
    )
    summary["es_los_rios"] = summary["Region_Normalizada"].eq(TARGET_REGION)
    summary = summary.sort_values("total_innova", ascending=False)
    summary["total_innova_mm"] = summary["total_innova"] / 1e6
    return summary


def select_top_regions(
    summary: pd.DataFrame,
    *,
    limit: int = 5,
    ensure_target: bool = True,
) -> list[str]:
    candidates = summary["Region_Normalizada"].head(limit).tolist()
    if ensure_target and TARGET_REGION not in candidates:
        candidates.append(TARGET_REGION)
    return list(dict.fromkeys(candidates))[:limit]


def build_region_color_map(
    regions: Sequence[str],
    *,
    highlight_color: str = PALETTE["los_rios"],
    other_colors: Iterable[str] | None = None,
) -> dict[str, str]:
    palette_iter = iter(other_colors or DEFAULT_COLOR_SEQUENCE)
    mapping: dict[str, str] = {}
    for region in regions:
        if region == TARGET_REGION:
            mapping[region] = highlight_color
        else:
            mapping[region] = next(palette_iter)
    return mapping


def build_yearly_region_projects(df: pd.DataFrame, regions: Sequence[str]) -> pd.DataFrame:
    filtered = df[df["Region_Normalizada"].isin(regions)]
    return (
        filtered.groupby(["anio_dt", "Region_Normalizada"])
        .size()
        .reset_index(name="proyectos")
    )


def build_panel_finance(df: pd.DataFrame, regions: Sequence[str]) -> pd.DataFrame:
    filtered = df[df["Region_Normalizada"].isin(regions)]
    return (
        filtered.groupby(["anio_dt", "Region_Normalizada"])
        .agg(
            total_innova=("Financiamiento Innova", "sum"),
            aporte_privado=("Aprobado Privado", "sum"),
        )
        .reset_index()
    )
