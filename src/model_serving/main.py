import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.model_serving.config import get_config
from src.model_serving.api.routes import predict, models, health
from src.model_serving.api.middleware import PrometheusMiddleware
from src.model_serving.versioning.manager import ModelManager

app = FastAPI(
    title="MLOps Model Serving Platform",
    description="Universal API for serving ML models with auto-scaling, A/B testing, and metrics.",
    version="0.1.0",
)

config = get_config()

# Setup Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware)

# Prometheus Metrics Endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Include Routers
app.include_router(health.router, tags=["Health"])
app.include_router(models.router, prefix="/models", tags=["Models"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])

@app.on_event("startup")
async def startup_event():
    # Initialize ModelManager
    manager = ModelManager.get_instance()
    await manager.load_models(config.models)

if __name__ == "__main__":
    uvicorn.run(
        "src.model_serving.main:app",
        host=config.server.host,
        port=config.server.port,
        workers=config.server.workers,
        log_level=config.server.log_level.lower(),
        reload=False
    )
