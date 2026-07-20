# NeuroCRM - Plataforma Inteligente de Gestión Inmobiliaria

Este repositorio contiene el código fuente, la infraestructura y los pipelines de automatización de NeuroCRM, un sistema diseñado para optimizar la gestión de prospectos (leads) y predecir el riesgo de abandono (churn) en pequeñas y medianas inmobiliarias.

Toda la solución ha sido construida bajo un enfoque técnico 100% local (localhost) y de código abierto, garantizando la autonomía total de los datos y un costo cero en licencias de software, en estricto cumplimiento con los requisitos de la asignatura.

## 🏗️ Stack Tecnológico

- **Orquestador de Flujos y Eventos:** n8n (Local Self-Hosted)
- **Módulo Inteligente (IA):** Red Neuronal Perceptrón Multicapa (MLP) expuesto con FastAPI
- **Plataforma MLOps:** MLflow (Servidor de Tracking y Model Registry local)
- **Base de Datos:** PostgreSQL 15
- **Simulador de Salida SMTP:** Mailpit (Pruebas de correo locales sin costo)

## 📁 Estructura del Repositorio

El proyecto sigue una arquitectura limpia y separada por responsabilidades funcionales:

- **/ia-module:** Contiene el backend de FastAPI (`main.py`), el Dockerfile del microservicio, el script de entrenamiento (`train.py`), los artefactos de MLflow (`.pkl`) y el dataset.
- **/dataset:** Fuentes originales, datos procesados y scripts reproducibles del Entregable 6.
- **/tests:** Payloads, ejecutores, matrices de resultados y evidencias de pruebas.
- **/docs:** Informe técnico del Entregable 6.
- **/workflows:** Flujos y pipelines lógicos estructurados, listos para ser importados en n8n (.json).
- **/database:** Archivos de inicialización y esquemas de tablas SQL para la base de datos local.
- **docker-compose.yml:** Manifiesto central que orquesta, interconecta y aisla en red todos los servicios de la plataforma.

## 🚀 Instrucciones para Levantar el Entorno Local

### Prerrequisitos

- Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) y Docker Compose.
- Tener Git configurado.

### Despliegue de la Infraestructura

1. Clona este repositorio:
   ```bash
   git clone [https://github.com/Mr20DL/neurocrm-platform.git](https://github.com/Mr20DL/neurocrm-platform.git)
   cd neurocrm-platform
   ```
2. Levanta y construye todos los servicios en segundo plano automáticamente:
   ```bash
   docker compose up --build -d
   ```
3. Verificación de los Servicios en el Navegador

Una vez que Docker inicialice los contenedores, valide que las interfaces web y APIs respondan correctamente en las siguientes direcciones de su localhost:

- **n8n Core:** http://localhost:5678 (Orquestación de flujos)
- **FastAPI IA (Swagger Docs):** http://localhost:8000/docs (Para probar los endpoints /predict/lead-score y /predict/churn)
- **Mailpit UI:** http://localhost:8025 (Bandeja de entrada local para revisar correos enviados por n8n)
- **MLflow UI:** http://localhost:5000 (Servidor de Tracking y ciclo MLOps)

4. Ejecución del Ciclo de MLOps (Entrenamiento Opcional)

Si desea volver a entrenar el Perceptrón Multicapa y registrar nuevas métricas en el servidor de MLflow, puede hacerlo de forma local:

```bash
cd ia-module
python -m venv venv
# Activar según OS (Windows: .\venv\Scripts\activate / Linux-Mac: source venv/bin/activate)
pip install -r requirements.txt
python train.py
```

Nota: El microservicio de producción en Docker lee directamente los artefactos .pkl generados por el pipeline bajo las variables de entorno configuradas.

## 👥 Integrantes del Grupo

- **Bruno Chochoca**
- **Bruno Pumapillo**
- **Kiltom Adolfo**
- **Carlos Montenegro**
