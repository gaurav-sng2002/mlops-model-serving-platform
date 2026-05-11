import onnxruntime as ort
import numpy as np
from typing import Any, Dict, List
from .base import BaseModelLoader

class ONNXLoader(BaseModelLoader):
    def load(self, path: str) -> Any:
        # Load the ONNX model
        providers = ['CPUExecutionProvider']
        device = self.config.get("device", "auto")
        if device in ["cuda", "auto"] and "CUDAExecutionProvider" in ort.get_available_providers():
            providers.insert(0, "CUDAExecutionProvider")
            
        self.model = ort.InferenceSession(path, providers=providers)
        self.input_name = self.model.get_inputs()[0].name
        return self.model

    def predict(self, inputs: List[Any]) -> List[Any]:
        if not self.model:
            raise ValueError("Model not loaded")
            
        X = np.array(inputs, dtype=np.float32)
        outputs = self.model.run(None, {self.input_name: X})
        return outputs[0].tolist()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "framework": "onnx",
            "providers": self.model.get_providers() if self.model else []
        }
