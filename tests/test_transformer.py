"""Unit tests for the ProjectTransformer logic."""

from __future__ import annotations

import pandas as pd

from src.core.config import BooleanMapping, EtlSettings
from src.etl.transform import ProjectTransformer


def test_project_transformer_clean_currency_boolean_and_dates() -> None:
    settings = EtlSettings(
        chunk_size=1000,
        currency_columns=["Financiamiento Innova"],
        date_columns=["Inicio Actividad Económica"],
        boolean_mappings=BooleanMapping(affirmative=["Sí"], negative=["No"]),
    )
    transformer = ProjectTransformer(settings)

    frame = pd.DataFrame(
        {
            "Financiamiento Innova": ["$1.000"],
            "Inicio Actividad Económica": ["2010-01-01 00:00:00"],
            "Criterio Mujer": ["Sí"],
            "Título": ["  Proyecto   piloto  "],
        }
    )

    result = transformer.transform(frame)

    assert result["Financiamiento Innova"].iloc[0] == 1000
    assert str(result["Inicio Actividad Económica"].iloc[0]) == "2010-01-01 00:00:00"
    assert bool(result["Criterio Mujer"].iloc[0]) is True
    assert result["Título"].iloc[0] == "Proyecto piloto"
