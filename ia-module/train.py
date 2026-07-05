import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Configurar MLflow para que apunte al contenedor local
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("NeuroCRM_Lead_Scoring")

# 2. Dataset Sintético (Ejemplo: [Presupuesto_Estandarizado, Zona_Interes_Id, Cant_Habitaciones])
# Datos de entrenamiento simulados: 100 leads
X = np.random.rand(100, 3) 
y = np.random.choice([0, 1], size=100) # 0 = Frío, 1 = Caliente

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Parámetros del Perceptrón Multicapa (MLP)
hidden_layers = (10, 5)
lr = 0.01

with mlflow.start_run():
    # Entrenar Red Neuronal
    mlp = MLPClassifier(hidden_layer_sizes=hidden_layers, learning_rate_init=lr, max_iter=500, random_state=42)
    mlp.fit(X_train, y_train)
    
    # Evaluar
    predictions = mlp.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    
    # --- MLOps: Registrar en MLflow ---
    mlflow.log_param("hidden_layer_sizes", hidden_layers)
    mlflow.log_param("learning_rate", lr)
    mlflow.log_metric("accuracy", acc)
    
    # Guardar el modelo en el registro local
    mlflow.sklearn.log_model(mlp, name="mlp_lead_model", serialization_format=mlflow.sklearn.SERIALIZATION_FORMAT_CLOUDPICKLE,)
    
    print(f"Modelo entrenado con éxito. Accuracy: {acc}. Registrado en MLflow UI.")
