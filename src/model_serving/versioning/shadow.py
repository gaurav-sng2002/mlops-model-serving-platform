import asyncio
import logging
from typing import Any, List
from src.model_serving.engine.predictor import Predictor

logger = logging.getLogger(__name__)

class ShadowDeployer:
    def __init__(self, shadow_predictor: Predictor):
        self.predictor = shadow_predictor

    def run_shadow(self, inputs: List[Any]):
        """Run inference on the shadow model asynchronously without affecting the main response."""
        asyncio.create_task(self._run_async(inputs))

    async def _run_async(self, inputs: List[Any]):
        try:
            loop = asyncio.get_event_loop()
            predictions = await loop.run_in_executor(None, self.predictor.predict, inputs)
            # Log the predictions for offline analysis
            logger.info({
                "action": "shadow_predict",
                "model": self.predictor.model_name,
                "version": self.predictor.version,
                "predictions": predictions
            })
        except Exception as e:
            logger.error(f"Shadow prediction failed: {e}")
