import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.model_serving.monitoring.metrics import HTTP_REQUESTS, HTTP_LATENCY

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        
        # Exclude metrics endpoint from tracking to avoid noise
        if endpoint == "/metrics":
            return await call_next(request)
            
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status = str(response.status_code)
        except Exception as e:
            status = "500"
            raise e
        finally:
            duration = time.time() - start_time
            HTTP_REQUESTS.labels(method=method, endpoint=endpoint, status=status).inc()
            HTTP_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)
            
        return response
