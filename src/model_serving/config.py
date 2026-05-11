import os
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import yaml

class ApiKey(BaseModel):
    name: str
    key: str
    rate_limit: str

class AuthConfig(BaseModel):
    enabled: bool = False
    api_keys: List[ApiKey] = []

class RollbackConfig(BaseModel):
    error_threshold: float = 0.05
    latency_threshold_ms: int = 500
    window_seconds: int = 60

class VersioningConfig(BaseModel):
    enabled: bool = False
    rollback: RollbackConfig = RollbackConfig()

class BatchingConfig(BaseModel):
    enabled: bool = False
    max_batch_size: int = 32
    timeout_ms: int = 10

class ModelConfig(BaseModel):
    name: str
    source: str = "local"
    path: str
    framework: str = "auto"
    device: str = "auto"
    warmup: bool = True
    weight: int = 100

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    log_level: str = "info"

class AppConfig(BaseSettings):
    server: ServerConfig = ServerConfig()
    auth: AuthConfig = AuthConfig()
    versioning: VersioningConfig = VersioningConfig()
    batching: BatchingConfig = BatchingConfig()
    models: List[ModelConfig] = []

    @classmethod
    def load_from_yaml(cls, path: str) -> "AppConfig":
        with open(path, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

def get_config() -> AppConfig:
    config_path = os.getenv("MODEL_SERVING_CONFIG", "config/default.yaml")
    if os.path.exists(config_path):
        return AppConfig.load_from_yaml(config_path)
    return AppConfig()
