import logging
import json
import time
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        
        # Add any extra attributes
        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id
        if hasattr(record, "model"):
            log_obj["model"] = record.model
        if hasattr(record, "latency_ms"):
            log_obj["latency_ms"] = record.latency_ms
            
        return json.dumps(log_obj)

def setup_logging(level: str = "INFO"):
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))
    
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    # Remove existing handlers
    for h in logger.handlers[:]:
        logger.removeHandler(h)
        
    logger.addHandler(handler)
