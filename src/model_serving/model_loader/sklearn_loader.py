import joblib
import numpy as np
from typing import Any, Dict, List
from .base import BaseModelLoader

class SklearnLoader(BaseModelLoader):
    def load(self, path: str) -> Any:
        self.model = joblib.load(path)
        if self.config.get("warmup", True):
            # Try to warm up with dummy data if possible, or just skip
            pass
        return self.model

    def predict(self, inputs: List[Any]) -> List[Any]:
        if not self.model:
            raise ValueError("Model not loaded")
        # Convert list of dicts or list of lists to numpy array
        if isinstance(inputs[0], dict):
            # Very basic extraction, in reality needs schema
            X = np.array([[v for v in item.values()] for item in inputs])
        else:
            X = np.array(inputs)
        
        predictions = self.model.predict(X)
        return predictions.tolist()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "framework": "sklearn",
            "type": type(self.model).__name__
        }
