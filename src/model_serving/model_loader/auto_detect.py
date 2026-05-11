import os
import logging
from typing import Dict, Any

from src.model_serving.model_loader.base import BaseModelLoader

logger = logging.getLogger(__name__)

def load_model(config: Dict[str, Any]) -> BaseModelLoader:
    framework = config.get("framework", "auto")
    path = config.get("path", "")
    
    if framework == "auto":
        ext = os.path.splitext(path)[1].lower()
        if ext in [".pkl", ".joblib"]:
            framework = "sklearn"
        elif ext in [".pt", ".pth"]:
            framework = "pytorch"
        elif ext in [".h5", ".pb"] or os.path.isdir(path):
            framework = "tensorflow"
        elif ext in [".json", ".ubj"] and "xgb" in path:
            framework = "xgboost"
        elif ext in [".onnx"]:
            framework = "onnx"
        else:
            raise ValueError(f"Could not auto-detect framework for path: {path}")
            
    logger.info(f"Loading model with framework: {framework} from {path}")
    
    if framework == "sklearn":
        from .sklearn_loader import SklearnLoader
        loader = SklearnLoader(config)
    elif framework == "pytorch":
        from .pytorch_loader import PyTorchLoader
        loader = PyTorchLoader(config)
    elif framework == "tensorflow":
        from .tensorflow_loader import TensorFlowLoader
        loader = TensorFlowLoader(config)
    elif framework == "xgboost":
        from .xgboost_loader import XGBoostLoader
        loader = XGBoostLoader(config)
    elif framework == "onnx":
        from .onnx_loader import ONNXLoader
        loader = ONNXLoader(config)
    else:
        raise ValueError(f"Unsupported framework: {framework}")
        
    loader.load(path)
    return loader
