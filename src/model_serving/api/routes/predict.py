from fastapi import APIRouter, Depends, Request, HTTPException
from src.model_serving.api.schemas import PredictRequest, PredictResponse
from src.model_serving.api.auth import verify_api_key
from src.model_serving.versioning.manager import ModelManager
from src.model_serving.versioning.ab_router import ABRouter

router = APIRouter()
router.dependencies = [Depends(verify_api_key)]
router_strategy = ABRouter()

@router.post("", response_model=PredictResponse)
async def predict(request: Request, body: PredictRequest):
    manager = ModelManager.get_instance()
    
    try:
        # Determine version using A/B routing
        version = router_strategy.route_request(
            model_name=body.model_name,
            headers=dict(request.headers),
            user_id=body.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    batcher = manager.get_batcher(body.model_name, version)
    
    if batcher:
        # Use batching
        predictions = []
        for input_data in body.inputs:
            pred = await batcher.predict_async(input_data)
            predictions.append(pred)
    else:
        # Synchronous prediction
        predictor = manager.get_predictor(body.model_name, version)
        if not predictor:
            raise HTTPException(status_code=500, detail="Predictor not initialized")
        predictions = predictor.predict(body.inputs)
        
    return PredictResponse(
        model_name=body.model_name,
        version=version,
        predictions=predictions
    )
