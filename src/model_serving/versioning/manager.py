import logging
from typing import Dict, List, Any, Optional
from src.model_serving.model_loader.auto_detect import load_model
from src.model_serving.engine.predictor import Predictor
from src.model_serving.engine.batcher import DynamicBatcher
from src.model_serving.config import ModelConfig, get_config
from src.model_serving.monitoring.metrics import MODEL_LOADED

logger = logging.getLogger(__name__)

class ModelManager:
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance
        
    def __init__(self):
        self.config = get_config()
        # model_name -> version -> {loader, predictor, batcher, metadata}
        self.models: Dict[str, Dict[str, Dict[str, Any]]] = {}
        
    async def load_models(self, models_config: List[ModelConfig]):
        for model_cfg in models_config:
            await self.load_model(model_cfg)
            
    async def load_model(self, model_cfg: ModelConfig):
        name = model_cfg.name
        # Use path as version identifier if not explicitly versioned
        version = model_cfg.path.split('/')[-1].split('.')[0] 
        
        logger.info(f"Loading model {name} version {version}")
        
        try:
            config_dict = model_cfg.dict()
            loader = load_model(config_dict)
            predictor = Predictor(loader, name, version)
            
            batcher = None
            if self.config.batching.enabled:
                batcher = DynamicBatcher(
                    predictor, 
                    max_batch_size=self.config.batching.max_batch_size,
                    timeout_ms=self.config.batching.timeout_ms
                )
                
            if name not in self.models:
                self.models[name] = {}
                
            self.models[name][version] = {
                "loader": loader,
                "predictor": predictor,
                "batcher": batcher,
                "metadata": {
                    "framework": model_cfg.framework,
                    "source": model_cfg.source,
                    "weight": model_cfg.weight
                }
            }
            
            MODEL_LOADED.labels(model=name, version=version).set(1)
            logger.info(f"Successfully loaded model {name}:{version}")
            
        except Exception as e:
            logger.error(f"Failed to load model {name}:{version}: {str(e)}")
            raise e

    def get_model_versions(self, name: str) -> Dict[str, Any]:
        return self.models.get(name, {})

    def get_model_metadata(self, name: str, version: str) -> Dict[str, Any]:
        return self.models.get(name, {}).get(version, {}).get("metadata", {})

    def get_predictor(self, name: str, version: str) -> Optional[Predictor]:
        return self.models.get(name, {}).get(version, {}).get("predictor")

    def get_batcher(self, name: str, version: str) -> Optional[DynamicBatcher]:
        return self.models.get(name, {}).get(version, {}).get("batcher")

    def unload_model(self, name: str, version: str = None):
        if name in self.models:
            if version:
                if version in self.models[name]:
                    del self.models[name][version]
                    MODEL_LOADED.labels(model=name, version=version).set(0)
            else:
                for v in list(self.models[name].keys()):
                    MODEL_LOADED.labels(model=name, version=v).set(0)
                del self.models[name]
