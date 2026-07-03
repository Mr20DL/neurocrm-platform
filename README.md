# NeuroCRM - Plataforma Inteligente de Gestión Inmobiliaria

Este repositorio contiene el código fuente, la infraestructura y los pipelines de automatización de NeuroCRM, un sistema diseñado para optimizar la gestión de prospectos (leads) y predecir el riesgo de abandono (churn) en pequeñas y medianas inmobiliarias.

Toda la solución ha sido construida bajo un enfoque técnico 100% local (localhost) y de código abierto, garantizando la autonomía total de los datos y un costo cero en licencias de software, en estricto cumplimiento con los requisitos de la asignatura.

## 🏗️ Stack Tecnológico

- **Orquestador de Flujos y Eventos:** n8n (Local Self-Hosted)
- **Módulo Inteligente (IA):** Red Neuronal Perceptrón Multicapa (MLP) en Python
- **Plataforma MLOps:** MLflow (Servidor de Tracking y Model Registry local)
- **Base de Datos:** PostgreSQL 15

## 📁 Estructura del Repositorio

El proyecto sigue una arquitectura limpia y separada por responsabilidades funcionales:

- **/ia-module:** Contiene el script de entrenamiento (train.py), la definición del dataset sintético y las dependencias de Python del Perceptrón Multicapa.
- **/workflows:** Flujos y pipelines lógicos estructurados, listos para ser importados en n8n (.json).
- **/database:** Archivos de inicialización y esquemas de tablas SQL para la base de datos local.
- **docker-compose.yml:** Manifiesto central que orquesta e interconecta todos los servicios de la plataforma.

## 🚀 Instrucciones para Levantar el Entorno Local

### Prerrequisitos

- Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) y Docker Compose.
- Tener Python 3.10 o superior (para ejecutar el entrenamiento del módulo de IA).

### Despliegue de la Infraestructura

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Mr20DL/neurocrm-platform.git
   cd neurocrm-platform
   ```
2. Levanta todos los servicios en segundo plano:
   ```bash
   docker compose up -d
   ```
3. Verificación de los Servicios en el Navegador

Una vez que Docker inicialice los contenedores, valide que las interfaces web respondan correctamente en las siguientes direcciones de su localhost:

- **n8n Core:** http://localhost:5678
- **MLflow UI:** http://localhost:5000

4. Ejecución del Ciclo de MLOps (Entrenamiento e Instrumentación)

Para ejecutar el Perceptrón Multicapa y registrar los hiperparámetros y métricas (Accuracy) en el servidor local de MLOps, siga estos pasos:

```bash
cd ia-module
pip install -r requirements.txt
python train.py
```

Al finalizar la ejecución, podrá visualizar y comparar las diferentes corridas y versiones del modelo directamente en la interfaz de MLflow UI.

## 👥 Integrantes del Grupo

- **Bruno Chochoca (Líder / Infraestructura)**
- **Bruno Pumapillo (Módulo Inteligente / IA)**
- **Kiltom Adolfo (Automatización / n8n)**
- **Carlos Montenegro (Arquitectura / Calidad)**
