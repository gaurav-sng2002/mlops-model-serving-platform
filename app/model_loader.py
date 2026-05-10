from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)
_IRIS_LABELS = {0: "setosa", 1: "versicolor", 2: "virginica"}


class ModelLoader:
    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self._model: Any = None

    def load(self) -> None:
        if self.model_path.exists():
            logger.info("Loading model from %s", self.model_path)
            self._model = joblib.load(self.model_path)
        else:
            logger.warning("Model not found at %s — training demo iris model", self.model_path)
            self._model = self._train_demo_model()

    def is_loaded(self) -> bool:
        return self._model is not None

    def predict(self, features: list[float]) -> tuple[int, str, float]:
        X = np.array(features).reshape(1, -1)
        prediction = int(self._model.predict(X)[0])
        probas = self._model.predict_proba(X)[0]
        confidence = float(probas[prediction])
        label = _IRIS_LABELS.get(prediction, str(prediction))
        return prediction, label, confidence

    @staticmethod
    def _train_demo_model() -> RandomForestClassifier:
        iris = load_iris()
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(iris.data, iris.target)
        os.makedirs("models", exist_ok=True)
        joblib.dump(clf, "models/model.joblib")
        return clf
