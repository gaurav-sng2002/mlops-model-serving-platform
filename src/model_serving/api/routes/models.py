from fastapi import APIRouter, Depends, HTTPException
from src.model_serving.api.auth import verify_api_key
from src.model_serving.versioning.manager import ModelManager
from src.model_serving.config import ModelConfig
from src.model_serving.api.schemas import ModelLoadRequest

router = APIRouter()
router.dependencies = [Depends(verify_api_key)]

@router.get("")
async def list_models():
    manager = ModelManager.get_instance()
    result = {}
    for name, versions in manager.models.items():
        result[name] = list(versions.keys())
    return result

@router.post("/reload")
async def load_model(request: ModelLoadRequest):
    manager = ModelManager.get_instance()
    cfg = ModelConfig(**request.dict())
    await manager.load_model(cfg)
    return {"status": "success", "message": f"Model {request.name} loaded"}

@router.get("/{name}/info")
async def get_model_info(name: str):
    manager = ModelManager.get_instance()
    versions = manager.get_model_versions(name)
    if not versions:
        raise HTTPException(status_code=404, detail="Model not found")
        
    return {
        "name": name,
        "versions": list(versions.keys()),
        "metadata": {v: manager.get_model_metadata(name, v) for v in versions.keys()}
    }

@router.delete("/{name}")
async def unload_model(name: str, version: str = None):
    manager = ModelManager.get_instance()
    if name not in manager.models:
        raise HTTPException(status_code=404, detail="Model not found")
        
    manager.unload_model(name, version)
    return {"status": "success", "message": f"Model {name} unloaded"}
