"""Ejecuta todos los payloads de churn y guarda evidencia JSON."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
URL = "http://localhost:8000/predict/churn"


def ejecutar(archivo: Path) -> dict[str, object]:
    payload = json.loads(archivo.read_text(encoding="utf-8"))
    request = urllib.request.Request(
        URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            status = response.status
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        status = error.code
        body = error.read().decode("utf-8")
    return {"caso": archivo.stem, "status_http": status, "entrada": payload, "respuesta": json.loads(body)}


def main() -> None:
    payloads = sorted((ROOT / "tests" / "payloads").glob("churn_*.json"))
    resultado = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": URL,
        "casos": [ejecutar(archivo) for archivo in payloads],
    }
    salida = ROOT / "tests" / "resultados" / "resultados_churn.json"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
