"""Valida los esquemas procesados de NeuroCRM."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def validar_leads(ruta: Path) -> None:
    columnas = [
        "presupuesto_min",
        "fuente_lead",
        "tipo_propiedad",
        "interacciones_iniciales",
        "conversion",
    ]
    df = pd.read_csv(ruta)
    if list(df.columns) != columnas:
        raise ValueError(f"Esquema de leads incorrecto: {list(df.columns)}")
    if df.empty or df.isnull().any().any():
        raise ValueError("El dataset de leads está vacío o contiene nulos.")
    if (df["presupuesto_min"] <= 0).any():
        raise ValueError("presupuesto_min debe ser mayor que cero.")
    if not df["fuente_lead"].isin([1, 2, 3]).all():
        raise ValueError("fuente_lead debe estar entre 1 y 3.")
    if not df["tipo_propiedad"].isin([1, 2, 3, 4]).all():
        raise ValueError("tipo_propiedad debe estar entre 1 y 4.")
    if (df["interacciones_iniciales"] < 0).any():
        raise ValueError("interacciones_iniciales no puede ser negativa.")
    if not df["conversion"].isin([0, 1]).all():
        raise ValueError("conversion debe ser binaria.")
    print(f"OK leads: {len(df)} registros; clases={df['conversion'].value_counts().to_dict()}")


def validar_churn(ruta: Path) -> None:
    columnas = [
        "antiguedad_meses",
        "dias_inactividad",
        "interacciones_30d",
        "quejas_registradas",
        "churn",
    ]
    df = pd.read_csv(ruta)
    if list(df.columns) != columnas:
        raise ValueError(f"Esquema de churn incorrecto: {list(df.columns)}")
    if df.empty or df.isnull().any().any():
        raise ValueError("El dataset de churn está vacío o contiene nulos.")
    for columna in columnas[:3]:
        if (df[columna] < 0).any():
            raise ValueError(f"{columna} no puede ser negativa.")
    if not df["quejas_registradas"].isin([0, 1]).all():
        raise ValueError("quejas_registradas debe ser binaria.")
    if not df["churn"].isin([0, 1]).all():
        raise ValueError("churn debe ser binaria.")
    print(f"OK churn: {len(df)} registros; clases={df['churn'].value_counts().to_dict()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-churn", action="store_true")
    args = parser.parse_args()
    validar_leads(ROOT / "dataset" / "processed" / "leads_neurocrm.csv")
    churn = ROOT / "dataset" / "processed" / "churn_neurocrm.csv"
    if churn.exists():
        validar_churn(churn)
    elif args.require_churn:
        raise FileNotFoundError(f"Falta el dataset procesado: {churn}")
    else:
        print("PENDIENTE churn: agrega dataset/raw/churn_original.csv y ejecuta preparar_churn.py")


if __name__ == "__main__":
    main()
