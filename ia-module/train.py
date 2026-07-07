import mlflow
import mlflow.sklearn
from ucimlrepo import fetch_ucirepo
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline


mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("NeuroCRM_Lead_Scoring")

# Dataset real y pequeño del dominio inmobiliario
real_estate = fetch_ucirepo(id=477)

X = real_estate.data.features.copy()
y = real_estate.data.targets.copy()

# Convertimos el precio de vivienda en una etiqueta binaria:
# 1 = valor alto, 0 = valor bajo
target_col = y.columns[0]
y = (y[target_col] >= y[target_col].median()).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# Variación 1 (Base)
hidden_layers = (32, 16)
learning_rate = 0.01

# Variación 2 (Deep / más capas, learning rate más bajo)
# hidden_layers = (16, 8)
# learning_rate = 0.005

# Variación 3 (Fast / menos capas, learning rate más alto)
# hidden_layers = (8, 4)
# learning_rate = 0.05

model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=hidden_layers,
        learning_rate_init=learning_rate,
        max_iter=500,
        random_state=42
    )
)

with mlflow.start_run():
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    mlflow.log_param("hidden_layer_sizes", str(hidden_layers))
    mlflow.log_param("learning_rate_init", learning_rate)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(
        model,
        "neurocrm_mlp_model",
        serialization_format="pickle"
    )

    print(f"Modelo entrenado con éxito. Accuracy: {accuracy}. Registrado en MLflow.")
