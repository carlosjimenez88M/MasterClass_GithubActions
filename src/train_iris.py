"""Pipeline de entrenamiento de un modelo de clasificacion sobre el dataset Iris."""

import os
import logging
import sys

import colorlog
import joblib
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------------
# Logger con colores tipo semaforo
# ---------------------------------------------------------------------------

def setup_logger(name: str = "iris_pipeline") -> logging.Logger:
    """Crea un logger con formato de colores tipo semaforo.

    Colores:
        - Verde  (INFO)     : operaciones exitosas, resultados.
        - Amarillo (WARNING) : precauciones o advertencias reales.
        - Rojo   (ERROR)    : fallos criticos.
    """
    logger = colorlog.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = colorlog.StreamHandler(stream=sys.stdout)
        handler.setFormatter(colorlog.ColoredFormatter(
            fmt="%(log_color)s[%(levelname)-8s]%(reset)s %(message)s",
            log_colors={
                "DEBUG":    "cyan",
                "INFO":     "green",
                "WARNING":  "yellow",
                "ERROR":    "red",
                "CRITICAL": "red,bg_white",
            },
        ))
        logger.addHandler(handler)

    return logger

# ---------------------------------------------------------------------------
# Funciones del pipeline
# ---------------------------------------------------------------------------

def load_data(logger: logging.Logger) -> tuple[pd.DataFrame, pd.Series]:
    """Carga el dataset Iris y lo devuelve como DataFrame/Series."""
    logger.info("Cargando dataset Iris...")
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name="target")
    logger.info("Dataset cargado: %d muestras, %d features.", len(X), X.shape[1])
    return X, y


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float,
    logger: logging.Logger,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Divide los datos en entrenamiento y prueba."""
    logger.info("Dividiendo datos (test_size=%.0f%%)...", test_size * 100)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42,
    )
    logger.info("Train: %d muestras | Test: %d muestras.", len(X_train), len(X_test))
    return X_train, X_test, y_train, y_test


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    logger: logging.Logger,
) -> RandomForestClassifier:
    """Entrena un clasificador RandomForest."""
    logger.info("Entrenando RandomForestClassifier (n_estimators=100)...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    logger.info("Entrenamiento finalizado.")
    return clf


def evaluate_model(
    clf: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    logger: logging.Logger,
) -> float:
    """Evalua el modelo y retorna el accuracy."""
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    logger.info("Accuracy: %.2f%%", acc * 100)

    report = classification_report(y_test, predictions)
    logger.info("Classification report:\n%s", report)

    return acc


def save_model(
    clf: RandomForestClassifier,
    output_dir: str,
    logger: logging.Logger,
) -> str:
    """Serializa el modelo a disco."""
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "iris_model.pkl")
    joblib.dump(clf, model_path)
    logger.info("Modelo guardado en: %s", model_path)
    return model_path

# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main() -> None:
    """Ejecuta el pipeline completo: carga -> split -> train -> eval -> save."""
    logger = setup_logger()
    logger.info("=== Inicio del pipeline de ML ===")

    try:
        X, y = load_data(logger)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, logger=logger)
        clf = train_model(X_train, y_train, logger)
        evaluate_model(clf, X_test, y_test, logger)
        save_model(clf, output_dir="models", logger=logger)
    except Exception as exc:
        logger.error("El pipeline fallo: %s", exc)
        raise

    logger.info("=== Pipeline finalizado con exito ===")


if __name__ == "__main__":
    main()
