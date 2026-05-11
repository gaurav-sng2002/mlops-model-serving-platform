from typing import Any, List, Dict
import time
from src.model_serving.model_loader.base import BaseModelLoader
from src.model_serving.monitoring.metrics import PREDICTION_TIME, PREDICTION_COUNT

class Predictor:
    def __init__(self, model_loader: BaseModelLoader, model_name: str, version: str):
        self.model_loader = model_loader
        self.model_name = model_name
        self.version = version

    def predict(self, inputs: List[Any]) -> List[Any]:
        start_time = time.time()
        
        try:
            predictions = self.model_loader.predict(inputs)
            status = "success"
        except Exception as e:
            status = "error"
            raise e
        finally:
            duration = time.time() - start_time
            PREDICTION_TIME.labels(model=self.model_name, version=self.version).observe(duration)
            PREDICTION_COUNT.labels(model=self.model_name, version=self.version, status=status).inc()
            
        return predictions
