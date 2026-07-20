# Pruebas de NeuroCRM

## Requisitos

- Docker Desktop activo.
- Servicios levantados con `docker compose up --build -d`.
- FastAPI accesible en `http://localhost:8000`.

## Validar datos

```powershell
python dataset/scripts/validar_datasets.py
```

## Ejecutar endpoints

```powershell
python tests/scripts/probar_lead_scoring.py
python tests/scripts/probar_churn.py
```

Los scripts recorren los JSON de `tests/payloads` y guardan la respuesta completa, el código HTTP y la fecha en `tests/resultados/*.json`.

## Contrato esperado

- Valores de dominio inválidos deben producir HTTP 422.
- Las probabilidades deben permanecer entre 0 y 100.
- Las respuestas exitosas deben mantener un esquema estable.
- Un fallo real debe documentarse; no debe cambiarse el resultado esperado para marcarlo como aprobado.

## Evidencias pendientes

- [ ] Confirmar contrato definitivo de FastAPI.
- [ ] Corregir las validaciones de dominio detectadas en `main.py`.
- [ ] Ejecutar todos los payloads con Docker activo.
- [ ] Guardar capturas de FastAPI/Postman o terminal.
- [ ] Guardar ejecución de n8n.
- [ ] Consultar y capturar el registro PostgreSQL.
- [ ] Completar resultados obtenidos y estados.
