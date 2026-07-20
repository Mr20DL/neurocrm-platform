# Entregable 6: Datos y pruebas de NeuroCRM

## 6.1 Objetivo

Este entregable documenta los conjuntos de datos utilizados para los modelos de Lead Scoring y churn, sus procesos reproducibles de preparación y validación, y los escenarios de prueba funcional de los endpoints del microservicio.

## 6.2 Dataset de Lead Scoring

Se utilizó un dataset público de conversión de prospectos de educación en línea. Contiene 9,240 registros, 37 variables originales y el target binario real `Converted`. La clase 0 contiene 5,679 registros (61.46 %) y la clase 1 contiene 3,561 (38.54 %).

La adaptación conserva el target real, usa `TotalVisits` como aproximación de interacciones iniciales y agrupa `Lead Source` en Web, recomendación y red social. Debido a que la fuente no incluye presupuesto ni tipo de propiedad, estos campos se generan sintéticamente con semilla 42 sin consultar el target.

### Resultado de preparación

| Métrica | Resultado |
| --- | ---: |
| Registros originales | 9,240 |
| IDs duplicados eliminados | 0 |
| Targets inválidos eliminados | 0 |
| `TotalVisits` nulos imputados | 137 |
| Mediana usada para `TotalVisits` | 3 |
| Registros finales | 9,240 |
| Clase 0 | 5,679 |
| Clase 1 | 3,561 |

## 6.3 Dataset de churn

El adaptador reproducible está implementado para el dataset Ecommerce Customer Churn. La ejecución queda pendiente hasta incorporar `dataset/raw/churn_original.csv`. No se generaron resultados ni cantidades ficticias.

La correspondencia prevista es `Tenure` → `antiguedad_meses`, `DaySinceLastOrder` → `dias_inactividad`, `OrderCount` → `interacciones_30d`, `Complain` → `quejas_registradas` y `Churn` → `churn`.

## 6.4 Limpieza y preparación

1. Lectura del CSV original.
2. Verificación de columnas obligatorias.
3. Eliminación de duplicados por `Prospect ID`.
4. Conversión del target y visitas a valores numéricos.
5. Imputación de visitas faltantes con la mediana.
6. Agrupación determinista de fuentes.
7. Generación sintética controlada de variables inmobiliarias.
8. Exportación con el esquema exacto del endpoint.
9. Validación de nulos, rangos, categorías y target binario.

## 6.5 Validación

La ejecución de `python dataset/scripts/validar_datasets.py` confirmó 9,240 filas válidas para Lead Scoring, sin nulos y con clases `{0: 5679, 1: 3561}`. Churn aparece explícitamente como pendiente hasta disponer de su fuente.

## 6.6 Estrategia de pruebas

Las pruebas se dividen en escenarios normales, extremos y erróneos. Los resultados esperados se definieron antes de ejecutar el sistema. Las respuestas reales deben registrarse sin alterarlas para ocultar fallos.

| ID | Módulo | Escenario | Resultado esperado | Estado actual |
| --- | --- | --- | --- | --- |
| LS-01 | Lead Scoring | Lead completo | HTTP 200, score 0–100 | Pendiente |
| LS-02 | Lead Scoring | Presupuesto cero | HTTP 422 | Pendiente; API actual lo acepta |
| LS-03 | Lead Scoring | Presupuesto negativo | HTTP 422 | Pendiente; API actual lo trunca |
| LS-04 | Lead Scoring | Campos faltantes | HTTP 422 | Pendiente |
| LS-05 | Lead Scoring | Tipo incorrecto | HTTP 422 | Pendiente |
| LS-06 | Lead Scoring | Categorías inválidas | HTTP 422 | Pendiente; API actual no limita categorías |
| CH-01 | Churn | Cliente normal | HTTP 200, probabilidad 0–100 | Pendiente |
| CH-02 | Churn | 180 días inactivo | HTTP 200 estable | Pendiente |
| CH-03 | Churn | Entrada inválida | HTTP 422 | Pendiente; faltan límites de dominio |

## 6.7 Hallazgos de integración

El microservicio actual no carga los modelos porque sus rutas contienen `...`. Además, los artefactos existentes esperan seis variables del dataset UCI de valoración inmobiliaria, mientras la API envía cuatro variables de prospectos o clientes. Hasta corregir el entrenamiento y las rutas, las respuestas provienen de fórmulas de respaldo.

## 6.8 Evidencias pendientes

Una vez corregido y levantado el Entregable 5 se deben guardar: payload, respuesta, código HTTP, captura de terminal/Postman, ejecución n8n, inserción PostgreSQL y log de FastAPI para cada caso representativo.

## 6.9 Limitaciones

- Los datasets públicos no provienen de una inmobiliaria peruana.
- Parte de las variables se adapta mediante equivalencia semántica.
- Presupuesto y tipo de propiedad son sintéticos.
- Los modelos son prototipos académicos y requieren datos históricos reales para producción.

## 6.10 Conclusión provisional

El paquete de Lead Scoring ya es reproducible y cumple el esquema de NeuroCRM. Quedan pendientes la incorporación del CSV real de churn, la alineación de los modelos del Entregable 5 y la captura de evidencias sobre el sistema ejecutándose.
