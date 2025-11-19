"""Generate an HTML version of the Los Ríos bar chart visualization.

This script mirrors the logic from ``notebooks/los_rios_viz.ipynb`` and exports the
Plotly figure into ``docs/`` using the internal ``ncnvert`` helper requested by the
user.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.ncnvert import figure_to_html
from src.viz.los_rios_data import PALETTE, TARGET_REGION, build_region_summary, load_dataset

DATA_PATH = PROJECT_ROOT / "data/processed/corfo_projects.csv"
OUTPUT_HTML = PROJECT_ROOT / "docs/los_rios_financiamiento_bar.html"


def build_bar_figure(summary: pd.DataFrame) -> go.Figure:
    bar_df = summary.copy()
    bar_df["color"] = np.where(bar_df["es_los_rios"], PALETTE["los_rios"], PALETTE["otras"])

    fig = go.Figure(
        go.Bar(
            x=bar_df["Region_Normalizada"],
            y=bar_df["total_innova_mm"],
            marker_color=bar_df["color"],
            text=bar_df["total_innova_mm"].round(1),
            textposition="outside",
            hovertemplate=(
                "Región: %{x}<br>Financiamiento: %{y:.1f} MM CLP<br>Proyectos: %{customdata}"
            ),
            customdata=bar_df["proyectos"],
        )
    )

    los_rios_row = bar_df[bar_df["es_los_rios"]]
    if not los_rios_row.empty:
        row = los_rios_row.iloc[0]
        fig.add_annotation(
            x=row["Region_Normalizada"],
            y=row["total_innova_mm"],
            text="Región de Los Ríos",
            showarrow=True,
            arrowcolor=PALETTE["los_rios"],
            arrowhead=2,
            ay=-80,
        )

    fig.update_layout(
        title="Financiamiento Innova por región (millones CLP)",
        xaxis_title="Región",
        yaxis_title="Financiamiento (MM CLP)",
        xaxis_tickangle=-35,
        bargap=0.25,
        margin=dict(l=40, r=20, t=60, b=120),
    )

    return fig


def main() -> None:
    dataset = load_dataset(DATA_PATH)
    summary = build_region_summary(dataset)
    figure = build_bar_figure(summary)
    figure_to_html(
        figure,
        OUTPUT_HTML,
        title="Financiamiento Innova por región",
    )
    print(f"Archivo HTML generado en {OUTPUT_HTML.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
