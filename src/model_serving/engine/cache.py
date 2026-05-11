import json
import hashlib
from typing import Any, Optional
import redis

class PredictionCache:
    def __init__(self, redis_url: str = None, enabled: bool = False, ttl_seconds: int = 3600):
        self.enabled = enabled
        self.ttl = ttl_seconds
        self.client = redis.from_url(redis_url) if redis_url and enabled else None

    def _hash_input(self, model_name: str, version: str, input_data: Any) -> str:
        data_str = json.dumps(input_data, sort_keys=True)
        key_str = f"{model_name}:{version}:{data_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, model_name: str, version: str, input_data: Any) -> Optional[Any]:
        if not self.enabled or not self.client:
            return None
        key = self._hash_input(model_name, version, input_data)
        cached = self.client.get(key)
        return json.loads(cached) if cached else None

    def set(self, model_name: str, version: str, input_data: Any, prediction: Any):
        if not self.enabled or not self.client:
            return
        key = self._hash_input(model_name, version, input_data)
        self.client.setex(key, self.ttl, json.dumps(prediction))
