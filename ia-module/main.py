import os
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="NeuroCRM AI Service", version="1.0")

# --- CONTROL DE RUTAS DE LOS MODELOS ---
# Si las variables de entorno no encuentran la ruta exacta, usamos rutas locales por defecto
PATH_SCORING = os.getenv("MODEL_PATH_SCORING", "mlartifacts/1/m-30fc4b534e1f4bec8e72aa32e10f7.../model.pkl")
PATH_CHURN = os.getenv("MODEL_PATH_CHURN", "mlartifacts/1/m-8907a2becb154fcd8d9b5e3009d7.../model.pkl")

# Variables globales para almacenar los modelos en memoria
model_scoring = None
model_churn = None

@app.on_event("startup")
def load_models():
    global model_scoring, model_churn
    try:
        # Reemplaza los '...' con tus hashes reales en producción o verifica la existencia del archivo
        if os.path.exists(PATH_SCORING):
            with open(PATH_SCORING, "rb") as f:
                model_scoring = pickle.load(f)
        else:
            print(f"Advertencia: No se encontró el archivo de Scoring en {PATH_SCORING}. Usando fallback.")

        if os.path.exists(PATH_CHURN):
            with open(PATH_CHURN, "rb") as f:
                model_churn = pickle.load(f)
        else:
            print(f"Advertencia: No se encontró el archivo de Churn en {PATH_CHURN}. Usando fallback.")
            
    except Exception as e:
        print(f"Error crítico al cargar los archivos .pkl: {str(e)}")

# --- MODELOS DE ENTRADA (Validación de Datos con Pydantic) ---
class LeadScoringInput(BaseModel):
    presupuesto_min: float
    fuente_lead: int
    tipo_propiedad: int
    interacciones_iniciales: int

class ChurnInput(BaseModel):
    antiguedad_meses: int
    dias_inactividad: int
    interacciones_30d: int
    quejas_registradas: int

# --- ENDPOINTS DE INFERENCIA ---

@app.post("/predict/lead-score")
def predict_lead_score(data: LeadScoringInput):
    # CASO LÍMITE: Control de datos erróneos/negativos
    presupuesto = data.presupuesto_min
    if presupuesto < 0:
        presupuesto = 0.0  # Truncamiento defensivo
        
    # Si el modelo real no cargó, simulamos la respuesta matemática del MLP (Sigmoide) 
    # para evitar que el flujo de n8n se rompa durante el desarrollo del grupo
    if model_scoring is None:
        # Inferencia simulada (Fallback estable)
        score_decimal = 1 / (1 + np.exp(- (presupuesto * 0.00001 + data.interacciones_iniciales * 0.5 - data.fuente_lead)))
    else:
        # Inferencia real usando el .pkl (Asegúrate de pasar las características en el orden de entrenamiento)
        features = np.array([[presupuesto, data.fuente_lead, data.tipo_propiedad, data.interacciones_iniciales]])
        score_decimal = float(model_scoring.predict_proba(features)[0][1]) # Si es Scikit-Learn

    score_porcentaje = int(round(score_decimal * 100))
    
    # Lógica de reglas de negocio asociadas
    prioridad = "BAJA"
    if score_porcentaje >= 80:
        prioridad = "ALTA (Hot Lead)"
    elif score_porcentaje >= 50:
        prioridad = "MEDIA"

    return {
        "status": "success",
        "score": score_porcentaje,
        "categoria": prioridad
    }

@app.post("/predict/churn")
def predict_churn(data: ChurnInput):
    # CASO LÍMITE: Inactividad extrema
    dias = data.dias_inactividad
    if dias < 0:
        dias = 0

    if model_churn is None:
        # Inferencia simulada basada en pesos lógicos (Fallback estable)
        churn_decimal = 1 / (1 + np.exp(- (dias * 0.05 + data.quejas_registradas * 2.0 - data.interacciones_30d * 0.3)))
    else:
        features = np.array([[data.antiguedad_meses, dias, data.interacciones_30d, data.quejas_registradas]])
        churn_decimal = float(model_churn.predict_proba(features)[0][1])

    churn_porcentaje = int(round(churn_decimal * 100))

    return {
        "status": "success",
        "probabilidad_churn": churn_porcentaje,
        "riesgo_abandono": "ALTO" if churn_porcentaje >= 70 else "BAJO"
    }