# Datos de NeuroCRM

Este directorio conserva el dato fuente separado de los archivos derivados.

## Lead Scoring

- Fuente: dataset público **Lead Scoring** de conversión de prospectos.
- Archivo original: `raw/lead_scoring_original.csv` (9,240 registros y 37 columnas).
- Target real: `Converted` (`0` no convirtió, `1` convirtió).
- Salida: `processed/leads_neurocrm.csv`.

La adaptación conserva `Converted`, aproxima `TotalVisits` como interacciones iniciales y agrupa `Lead Source` en tres canales. `presupuesto_min` y `tipo_propiedad` se generan con NumPy usando la semilla fija 42. Estas variables sintéticas no utilizan el target y, por tanto, no introducen fuga directa de `Converted`.

```powershell
python dataset/scripts/preparar_leads.py
python dataset/scripts/validar_datasets.py
```

## Churn

El repositorio ya contiene el adaptador, pero falta la fuente original. Colocar el dataset **Ecommerce Customer Churn** como `raw/churn_original.csv` y ejecutar:

```powershell
python dataset/scripts/preparar_churn.py
python dataset/scripts/validar_datasets.py --require-churn
```

El adaptador reconoce `Tenure`, `DaySinceLastOrder`, `OrderCount`, `Complain`/`Complaint` y `Churn`.

## Diccionarios finales

| Campo Lead Scoring | Significado |
| --- | --- |
| `presupuesto_min` | Presupuesto sintético positivo en unidades monetarias |
| `fuente_lead` | 1 Web, 2 WhatsApp/recomendación, 3 Instagram/red social |
| `tipo_propiedad` | 1 Departamento, 2 Casa, 3 Terreno, 4 Comercial |
| `interacciones_iniciales` | `TotalVisits`, con nulos imputados por la mediana |
| `conversion` | Target real del dataset original |

| Campo churn | Significado |
| --- | --- |
| `antiguedad_meses` | `Tenure` |
| `dias_inactividad` | `DaySinceLastOrder` |
| `interacciones_30d` | `OrderCount` como proxy |
| `quejas_registradas` | `Complain`/`Complaint` |
| `churn` | Target binario real |

## Limitaciones

- La fuente de leads pertenece a educación en línea, no a una inmobiliaria peruana.
- WhatsApp, Instagram, presupuesto y tipo de propiedad no existen exactamente en la fuente.
- Las equivalencias son apropiadas para un prototipo académico, no para producción.
- Antes de uso real se requiere reentrenamiento con históricos de una inmobiliaria.
