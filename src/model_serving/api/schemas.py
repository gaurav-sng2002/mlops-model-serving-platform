from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    model_name: str = Field(..., description="Name of the model to use")
    inputs: List[Any] = Field(..., description="List of input data points")
    user_id: Optional[str] = Field(None, description="Optional user ID for sticky A/B routing")

class PredictResponse(BaseModel):
    model_name: str
    version: str
    predictions: List[Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ModelLoadRequest(BaseModel):
    name: str
    source: str = "local"
    path: str
    framework: str = "auto"
    device: str = "auto"
    weight: int = 100
    
class ModelInfoResponse(BaseModel):
    name: str
    versions: List[str]
    active_version: str
    metadata: Dict[str, Any]
