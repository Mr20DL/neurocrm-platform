"""Adapta Ecommerce Customer Churn al contrato de NeuroCRM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "dataset" / "raw" / "churn_original.csv"
DEFAULT_OUTPUT = ROOT / "dataset" / "processed" / "churn_neurocrm.csv"

ALIASES = {
    "antiguedad_meses": ("Tenure", "tenure"),
    "dias_inactividad": ("DaySinceLastOrder", "DaysSinceLastOrder"),
    "interacciones_30d": ("OrderCount", "Order Count"),
    "quejas_registradas": ("Complain", "Complaint"),
    "churn": ("Churn", "churn"),
}


def encontrar_columna(columnas: list[str], candidatos: tuple[str, ...]) -> str:
    for candidato in candidatos:
        if candidato in columnas:
            return candidato
    raise ValueError(f"No se encontró ninguna columna compatible con {candidatos}")


def preparar(ruta_entrada: Path, ruta_salida: Path) -> dict[str, object]:
    if not ruta_entrada.exists():
        raise FileNotFoundError(
            f"Falta {ruta_entrada}. Coloca allí el CSV original de churn antes de ejecutar."
        )
    original = pd.read_csv(ruta_entrada)
    renombres = {
        encontrar_columna(list(original.columns), candidatos): destino
        for destino, candidatos in ALIASES.items()
    }
    df = original[list(renombres)].rename(columns=renombres).copy()
    for columna in df.columns:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")

    registros_originales = len(df)
    duplicados = int(df.duplicated().sum())
    nulos = int(df.isna().any(axis=1).sum())
    df = df.drop_duplicates().dropna().copy()
    for columna in ("antiguedad_meses", "dias_inactividad", "interacciones_30d"):
        df = df[df[columna] >= 0]
    df = df[df["quejas_registradas"].isin([0, 1])]
    df = df[df["churn"].isin([0, 1])]
    df = df.astype(int)

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta_salida, index=False)
    clases = df["churn"].value_counts().sort_index()
    return {
        "registros_originales": registros_originales,
        "duplicados_eliminados": duplicados,
        "filas_con_nulos_eliminadas": nulos,
        "registros_finales": len(df),
        "clase_0": int(clases.get(0, 0)),
        "clase_1": int(clases.get(1, 0)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(preparar(args.input, args.output), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
