from fastapi import APIRouter
from src.model_serving.versioning.manager import ModelManager

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/ready")
async def readiness_probe():
    manager = ModelManager.get_instance()
    if not manager.models:
        return {"status": "not_ready", "reason": "No models loaded"}
    return {"status": "ready"}
