import tensorflow as tf
import numpy as np
from typing import Any, Dict, List
from .base import BaseModelLoader

class TensorFlowLoader(BaseModelLoader):
    def load(self, path: str) -> Any:
        self.model = tf.keras.models.load_model(path)
        if self.config.get("warmup", True):
            pass
        return self.model

    def predict(self, inputs: List[Any]) -> List[Any]:
        if not self.model:
            raise ValueError("Model not loaded")
            
        tensor_inputs = tf.convert_to_tensor(inputs, dtype=tf.float32)
        outputs = self.model(tensor_inputs, training=False)
        return outputs.numpy().tolist()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "framework": "tensorflow"
        }
