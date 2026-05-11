from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from src.model_serving.config import get_config

config = get_config()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if not config.auth.enabled:
        return True
        
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )
        
    for key_cfg in config.auth.api_keys:
        if api_key == key_cfg.key:
            return True
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key"
    )
