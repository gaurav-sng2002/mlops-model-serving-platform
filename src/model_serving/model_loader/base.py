from abc import ABC, abstractmethod
from typing import Any, Dict, List

class BaseModelLoader(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None

    @abstractmethod
    def load(self, path: str) -> Any:
        """Load the model from the specified path"""
        pass

    @abstractmethod
    def predict(self, inputs: List[Any]) -> List[Any]:
        """Run predictions on the provided inputs"""
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Return model metadata (framework, version, expected inputs)"""
        pass
