"""Prepara el dataset público de Lead Scoring para el contrato de NeuroCRM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "dataset" / "raw" / "lead_scoring_original.csv"
DEFAULT_OUTPUT = ROOT / "dataset" / "processed" / "leads_neurocrm.csv"
SEED = 42


def mapear_fuente(valor: object) -> int:
    """Reduce los canales originales a los tres códigos aceptados por la API."""
    texto = str(valor).strip().lower()
    if any(token in texto for token in ("reference", "referral", "welingak")):
        return 2  # WhatsApp/recomendación como aproximación semántica.
    if any(token in texto for token in ("social", "facebook", "pay per click")):
        return 3  # Instagram/red social como aproximación semántica.
    return 1  # Web: búsqueda, tráfico directo, chat y fuentes desconocidas.


def preparar(ruta_entrada: Path, ruta_salida: Path) -> dict[str, object]:
    df = pd.read_csv(ruta_entrada)
    requeridas = {"Prospect ID", "Lead Source", "TotalVisits", "Converted"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas originales: {sorted(faltantes)}")

    registros_originales = len(df)
    duplicados = int(df.duplicated(subset=["Prospect ID"]).sum())
    df = df.drop_duplicates(subset=["Prospect ID"]).copy()

    df["Converted"] = pd.to_numeric(df["Converted"], errors="coerce")
    targets_invalidos = int((~df["Converted"].isin([0, 1])).sum())
    df = df[df["Converted"].isin([0, 1])].copy()

    visitas = pd.to_numeric(df["TotalVisits"], errors="coerce")
    nulos_visitas = int(visitas.isna().sum())
    mediana_visitas = float(visitas.median())
    visitas = visitas.fillna(mediana_visitas).clip(lower=0).round().astype(int)

    # Variables sintéticas específicas del dominio. No dependen del target Converted.
    rng = np.random.default_rng(SEED)
    presupuesto = rng.lognormal(mean=np.log(150_000), sigma=0.55, size=len(df))
    presupuesto = (np.round(presupuesto / 1_000) * 1_000).clip(50_000, 1_000_000)
    tipo_propiedad = rng.choice([1, 2, 3, 4], size=len(df), p=[0.45, 0.30, 0.20, 0.05])

    salida = pd.DataFrame(
        {
            "presupuesto_min": presupuesto.astype(int),
            "fuente_lead": df["Lead Source"].map(mapear_fuente).astype(int),
            "tipo_propiedad": tipo_propiedad.astype(int),
            "interacciones_iniciales": visitas,
            "conversion": df["Converted"].astype(int),
        }
    )

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    salida.to_csv(ruta_salida, index=False)

    clases = salida["conversion"].value_counts().sort_index()
    return {
        "entrada": str(ruta_entrada),
        "salida": str(ruta_salida),
        "registros_originales": registros_originales,
        "duplicados_eliminados": duplicados,
        "targets_invalidos_eliminados": targets_invalidos,
        "total_visits_nulos_imputados": nulos_visitas,
        "mediana_total_visits": mediana_visitas,
        "registros_finales": len(salida),
        "clase_0": int(clases.get(0, 0)),
        "clase_1": int(clases.get(1, 0)),
        "semilla_sintetica": SEED,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(preparar(args.input, args.output), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
