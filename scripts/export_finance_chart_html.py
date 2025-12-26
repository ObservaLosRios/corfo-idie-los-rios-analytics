"""Export the Los Ríos public financing figure into HTML."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.ncnvert import figure_to_html
from src.viz.los_rios_data import (
    SECONDARY_COLOR,
    TARGET_REGION,
    build_panel_finance,
    build_region_color_map,
    build_region_summary,
    load_dataset,
    select_top_regions,
)

DATA_PATH = PROJECT_ROOT / "data/processed/corfo_projects.csv"
PLOTLY_OUTPUT_HTML = PROJECT_ROOT / "docs/plotly_los_rios_financiamiento_innova.html"


def build_finance_figure(
    panel_finance: pd.DataFrame,
    top_regions: list[str],
    color_map: dict[str, str],
    metric_column: str,
    title: str,
    yaxis_title: str,
    annotate_peak: bool = False,
) -> go.Figure:
    frame = panel_finance.dropna(subset=["anio_dt"]).copy()
    fig = go.Figure()
    for region in top_regions:
        region_data = frame[frame["Region_Normalizada"] == region]
        display_name = "Región de Los Ríos" if region == TARGET_REGION else region
        fig.add_trace(
            go.Scatter(
                x=region_data["anio_dt"],
                y=region_data[metric_column] / 1e6,
                mode="lines+markers" if region == TARGET_REGION else "lines",
                name=display_name,
                line=dict(
                    color=color_map[region],
                    width=4 if region == TARGET_REGION else 2,
                    dash="solid" if region == TARGET_REGION else "dash",
                ),
                hovertemplate="%{x|%Y}: %{y:.1f} MM<extra>"
                + title
                + " - "
                + display_name
                + "</extra>",
            )
        )

    if annotate_peak:
        los_rios_data = frame[frame["Region_Normalizada"] == TARGET_REGION]
        if not los_rios_data.empty:
            peak_row = los_rios_data.loc[los_rios_data[metric_column].idxmax()]
            fig.add_annotation(
                x=peak_row["anio_dt"],
                y=peak_row[metric_column] / 1e6,
                text=f"Pico Los Ríos: {peak_row['anio_dt'].year} ({peak_row[metric_column] / 1e6:.1f} MM)",
                arrowhead=2,
                arrowcolor=SECONDARY_COLOR,
                ax=60,
                ay=-60,
                showarrow=True,
            )

    fig.update_layout(
        title=title,
        xaxis_title="Año",
        yaxis_title=yaxis_title,
        hovermode="x unified",
        legend_title="Región",
        height=400,
    )

    fig.update_xaxes(
        rangeselector=dict(
            buttons=[
                dict(count=3, label="3y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all", label="Todo"),
            ]
        ),
        rangeslider=dict(visible=True),
        type="date",
    )
    return fig


def main() -> None:
    dataset = load_dataset(DATA_PATH)
    summary = build_region_summary(dataset)
    top_regions = select_top_regions(summary)
    color_map = build_region_color_map(top_regions)
    panel_finance = build_panel_finance(dataset, top_regions)
    figure = build_finance_figure(
        panel_finance,
        top_regions,
        color_map,
        metric_column="total_innova",
        title="Financiamiento Innova (MM CLP)",
        yaxis_title="Monto (MM CLP)",
        annotate_peak=True,
    )
    figure_to_html(
        figure,
        PLOTLY_OUTPUT_HTML,
        title="Financiamiento Innova por región",
    )
    print(f"Archivo HTML (Plotly) generado en {PLOTLY_OUTPUT_HTML.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
