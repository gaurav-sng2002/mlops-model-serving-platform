import random
import hashlib
from typing import Dict, Optional, Any
from .manager import ModelManager

class ABRouter:
    def __init__(self):
        self.manager = ModelManager.get_instance()

    def route_request(self, model_name: str, headers: Dict[str, str] = None, user_id: str = None) -> str:
        """
        Determine which version of a model should handle the request.
        Priority:
        1. Explicit header (e.g., model-version: v2)
        2. User segment based on hash
        3. Weighted random choice (traffic splitting)
        """
        versions = self.manager.get_model_versions(model_name)
        if not versions:
            raise ValueError(f"Model {model_name} not found")
            
        if len(versions) == 1:
            return list(versions.keys())[0]

        # 1. Header-based routing
        if headers and "model-version" in headers:
            version = headers["model-version"]
            if version in versions:
                return version
                
        # Get weights
        weights_dict = {v: self.manager.get_model_metadata(model_name, v).get("weight", 100) 
                       for v in versions.keys()}
        
        # 2. User segment based on hash for sticky sessions
        if user_id:
            hash_val = int(hashlib.md5(f"{model_name}_{user_id}".encode()).hexdigest(), 16)
            total_weight = sum(weights_dict.values())
            if total_weight == 0:
                return list(versions.keys())[0]
                
            normalized_hash = hash_val % total_weight
            current_weight = 0
            for version, weight in weights_dict.items():
                current_weight += weight
                if normalized_hash < current_weight:
                    return version
                    
        # 3. Weighted random choice
        total_weight = sum(weights_dict.values())
        if total_weight == 0:
            return list(versions.keys())[0]
            
        r = random.uniform(0, total_weight)
        current_weight = 0
        for version, weight in weights_dict.items():
            current_weight += weight
            if r < current_weight:
                return version
                
        return list(versions.keys())[0]
