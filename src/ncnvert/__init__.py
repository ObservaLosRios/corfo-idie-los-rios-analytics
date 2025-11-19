"""Lightweight helpers to export Plotly objects as standalone HTML files.

The user requested to rely on an ``ncnvert`` library for HTML conversions, so this
module centralizes the logic instead of duplicating ``fig.to_html`` calls across
scripts and notebooks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

from plotly.graph_objects import Figure

PathLike = Union[str, Path]


def figure_to_html(
    figure: Figure,
    output_path: PathLike,
    *,
    title: str | None = None,
    include_plotlyjs: str | bool = "cdn",
    full_html: bool = True,
    auto_open: bool = False,
) -> Path:
    """Persist ``figure`` as an HTML document at ``output_path``.

    Parameters
    ----------
    figure:
        Plotly Figure instance to serialize.
    output_path:
        Target location for the HTML artifact. Parent directories are created
        automatically.
    title:
        Optional HTML ``<title>`` override for the generated document.
    include_plotlyjs:
        Forwarded to ``plotly.Figure.to_html`` to control how Plotly assets are
        embedded. Defaults to loading from the CDN to keep the file size small.
    full_html:
        Whether to emit a complete HTML document. Keeping the default ``True``
        makes the output easier to embed inside static hosting setups.
    auto_open:
        Open the generated file in the default browser when ``True``.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    html = figure.to_html(
        include_plotlyjs=include_plotlyjs,
        full_html=full_html,
        default_width="100%",
    )

    if title:
        html = html.replace(
            "<title>Plotly Figure</title>", f"<title>{title}</title>", 1
        )

    output_path.write_text(html, encoding="utf-8")

    if auto_open:
        import webbrowser  # Local import to avoid importing when unused.

        webbrowser.open(output_path.as_uri())

    return output_path
