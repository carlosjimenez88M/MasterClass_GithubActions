"""Tests unitarios para el pipeline de entrenamiento Iris."""

import os
import tempfile

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.train_iris import (
    load_data,
    split_data,
    train_model,
    evaluate_model,
    save_model,
    setup_logger,
)


logger = setup_logger("test_train")


class TestLoadData:
    def test_retorna_dataframe_y_series(self):
        X, y = load_data(logger)
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)

    def test_dimensiones_correctas(self):
        X, y = load_data(logger)
        assert X.shape == (150, 4)
        assert len(y) == 150


class TestSplitData:
    def test_proporciones(self):
        X, y = load_data(logger)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, logger=logger)
        assert len(X_test) == 30
        assert len(X_train) == 120


class TestTrainModel:
    def test_retorna_clasificador(self):
        X, y = load_data(logger)
        X_train, _, y_train, _ = split_data(X, y, test_size=0.2, logger=logger)
        clf = train_model(X_train, y_train, logger)
        assert isinstance(clf, RandomForestClassifier)


class TestEvaluateModel:
    def test_accuracy_superior_a_umbral(self):
        X, y = load_data(logger)
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, logger=logger)
        clf = train_model(X_train, y_train, logger)
        acc = evaluate_model(clf, X_test, y_test, logger)
        assert acc >= 0.90, f"Accuracy {acc:.2f} es demasiado baja"


class TestSaveModel:
    def test_archivo_creado(self):
        X, y = load_data(logger)
        X_train, _, y_train, _ = split_data(X, y, test_size=0.2, logger=logger)
        clf = train_model(X_train, y_train, logger)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = save_model(clf, output_dir=tmpdir, logger=logger)
            assert os.path.isfile(path)
            assert path.endswith(".pkl")
