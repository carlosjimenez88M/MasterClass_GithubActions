import os
import logging
import colorlog
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def setup_logger():
    # Configuracion del logger tipo semaforo
    logger = colorlog.getLogger()
    logger.setLevel(logging.INFO)
    
    # Prevenir que se agreguen multiples handlers si se corre varias veces
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        # Formato: Color del nivel + Mensaje
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s[%(levelname)s] %(message)s',
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            }
        ))
        logger.addHandler(handler)
    return logger

def main():
    logger = setup_logger()
    logger.info("Iniciando el entrenamiento del modelo Iris...")
    
    # 1. Cargar datos
    logger.info("Cargando el dataset...")
    try:
        iris = load_iris()
        X = pd.DataFrame(iris.data, columns=iris.feature_names)
        y = iris.target
    except Exception as e:
        logger.error(f"Error al cargar el dataset: {e}")
        return

    # 2. Dividir en train y test
    logger.warning("Dividiendo los datos en conjuntos de entrenamiento y prueba.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Entrenar modelo
    logger.warning("Entrenando el modelo RandomForest. Esto podria tomar un momento...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # 4. Evaluar
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    logger.info(f"Precision del modelo (Accuracy): {acc * 100:.2f}%")

    # 5. Guardar modelo
    os.makedirs("models", exist_ok=True)
    model_path = "models/iris_model.pkl"
    joblib.dump(clf, model_path)
    logger.info(f"Modelo guardado exitosamente en: {model_path}")

if __name__ == "__main__":
    main()
