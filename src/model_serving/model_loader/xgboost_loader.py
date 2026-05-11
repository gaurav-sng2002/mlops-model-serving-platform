import xgboost as xgb
import numpy as np
from typing import Any, Dict, List
from .base import BaseModelLoader

class XGBoostLoader(BaseModelLoader):
    def load(self, path: str) -> Any:
        self.model = xgb.Booster()
        self.model.load_model(path)
        return self.model

    def predict(self, inputs: List[Any]) -> List[Any]:
        if not self.model:
            raise ValueError("Model not loaded")
            
        if isinstance(inputs[0], dict):
            X = np.array([[v for v in item.values()] for item in inputs])
        else:
            X = np.array(inputs)
            
        dmatrix = xgb.DMatrix(X)
        predictions = self.model.predict(dmatrix)
        return predictions.tolist()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "framework": "xgboost"
        }
