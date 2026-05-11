import torch
from typing import Any, Dict, List
from .base import BaseModelLoader

class PyTorchLoader(BaseModelLoader):
    def load(self, path: str) -> Any:
        device_str = self.config.get("device", "auto")
        if device_str == "auto":
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")
        else:
            self.device = torch.device(device_str)
            
        self.model = torch.load(path, map_location=self.device)
        self.model.eval()
        
        if self.config.get("warmup", True):
            pass # TODO: implementation depends on input shape
        return self.model

    def predict(self, inputs: List[Any]) -> List[Any]:
        if not self.model:
            raise ValueError("Model not loaded")
            
        # Basic conversion to tensor
        with torch.no_grad():
            tensor_inputs = torch.tensor(inputs, dtype=torch.float32).to(self.device)
            outputs = self.model(tensor_inputs)
            return outputs.cpu().numpy().tolist()

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "framework": "pytorch",
            "device": str(self.device)
        }
