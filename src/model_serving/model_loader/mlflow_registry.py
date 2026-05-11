import mlflow
from typing import Any, Dict
import logging
from src.model_serving.model_loader.auto_detect import load_model
from src.model_serving.model_loader.base import BaseModelLoader

logger = logging.getLogger(__name__)

class MLflowRegistryLoader:
    @staticmethod
    def load(config: Dict[str, Any]) -> BaseModelLoader:
        model_uri = config.get("path")
        logger.info(f"Downloading model from MLflow: {model_uri}")
        local_path = mlflow.artifacts.download_artifacts(artifact_uri=model_uri)
        
        # Override path to local path and use auto-detect
        local_config = config.copy()
        local_config["path"] = local_path
        
        return load_model(local_config)
