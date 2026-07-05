from ucimlrepo import fetch_ucirepo
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

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

hidden_layers = (32, 16)
learning_rate = 0.01

model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=hidden_layers,
        learning_rate_init=learning_rate,
        max_iter=500,
        random_state=42
    )
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Modelo entrenado con éxito. Accuracy: {accuracy}")