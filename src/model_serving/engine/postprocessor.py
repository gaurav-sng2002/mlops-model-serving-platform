from typing import Any, List

class Postprocessor:
    def __init__(self, config: dict):
        self.config = config

    def process(self, predictions: List[Any]) -> List[Any]:
        # Simple passthrough for now, can be extended based on config
        return predictions
