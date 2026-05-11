import boto3
import os
import logging
from urllib.parse import urlparse
from typing import Any, Dict
from src.model_serving.model_loader.auto_detect import load_model
from src.model_serving.model_loader.base import BaseModelLoader

logger = logging.getLogger(__name__)

class S3Loader:
    @staticmethod
    def load(config: Dict[str, Any]) -> BaseModelLoader:
        s3_uri = config.get("path")
        logger.info(f"Downloading model from S3: {s3_uri}")
        
        parsed = urlparse(s3_uri)
        bucket = parsed.netloc
        key = parsed.path.lstrip('/')
        
        local_path = f"/tmp/{os.path.basename(key)}"
        
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, local_path)
        
        local_config = config.copy()
        local_config["path"] = local_path
        
        return load_model(local_config)
