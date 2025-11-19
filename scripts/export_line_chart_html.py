"""Export the time-series line chart from the notebook into an HTML artifact."""

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
	TARGET_REGION,
	build_region_color_map,
	build_region_summary,
	build_yearly_region_projects,
	load_dataset,
	select_top_regions,
)

DATA_PATH = PROJECT_ROOT / "data/processed/corfo_projects.csv"
OUTPUT_HTML = PROJECT_ROOT / "docs/los_rios_proyectos_line.html"


def build_line_chart(
	yearly_projects: pd.DataFrame,
	top_regions: list[str],
	color_map: dict[str, str],
) -> go.Figure:
	fig = go.Figure()
	for region in top_regions:
		region_data = yearly_projects[yearly_projects["Region_Normalizada"] == region]
		display_name = "Región de Los Ríos" if region == TARGET_REGION else region
		fig.add_trace(
			go.Scatter(
				x=region_data["anio_dt"],
				y=region_data["proyectos"],
				mode="lines+markers" if region == TARGET_REGION else "lines",
				name=display_name,
				line=dict(
					color=color_map[region],
					width=4 if region == TARGET_REGION else 2,
					dash="solid" if region == TARGET_REGION else "dash",
				),
				hovertemplate="Año %{x|%Y}<br>Proyectos %{y}<extra>"
				+ display_name
				+ "</extra>",
			)
		)

	fig.update_layout(
		title="Conteo de proyectos adjudicados por año (Top regiones)",
		xaxis_title="Año",
		yaxis_title="Número de proyectos",
		legend_title="Región",
	)
	return fig


def main() -> None:
	dataset = load_dataset(DATA_PATH)
	summary = build_region_summary(dataset)
	top_regions = select_top_regions(summary)
	color_map = build_region_color_map(top_regions)
	yearly_projects = build_yearly_region_projects(dataset, top_regions)
	figure = build_line_chart(yearly_projects, top_regions, color_map)
	figure_to_html(figure, OUTPUT_HTML, title="Conteo anual de proyectos")
	print(f"Archivo HTML generado en {OUTPUT_HTML.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
	main()
