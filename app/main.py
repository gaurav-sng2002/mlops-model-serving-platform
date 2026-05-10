from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from starlette.responses import Response

from app.model_loader import ModelLoader

REQUEST_COUNT = Counter("predict_requests_total", "Total prediction requests", ["status"])
REQUEST_LATENCY = Histogram(
    "predict_latency_seconds", "Prediction latency",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)

loader: ModelLoader | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global loader
    loader = ModelLoader(os.getenv("MODEL_PATH", "models/model.joblib"))
    loader.load()
    yield
    loader = None


app = FastAPI(title="MLOps Model Serving Platform", version=os.getenv("MODEL_VERSION", "1.0.0"), lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class PredictRequest(BaseModel):
    features: list[float]


class PredictResponse(BaseModel):
    prediction: int | str
    label: str
    confidence: float
    model_version: str
    latency_ms: int


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str


@app.get("/health", response_model=HealthResponse, tags=["ops"])
def health():
    return HealthResponse(
        status="ok",
        model_loaded=loader is not None and loader.is_loaded(),
        model_version=os.getenv("MODEL_VERSION", "1.0.0"),
    )


@app.get("/metrics", tags=["ops"])
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(body: PredictRequest):
    if loader is None or not loader.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    t0 = time.monotonic()
    try:
        prediction, label, confidence = loader.predict(body.features)
        REQUEST_COUNT.labels(status="ok").inc()
    except Exception as exc:
        REQUEST_COUNT.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        REQUEST_LATENCY.observe(time.monotonic() - t0)
    return PredictResponse(
        prediction=prediction, label=label,
        confidence=round(confidence, 4),
        model_version=os.getenv("MODEL_VERSION", "1.0.0"),
        latency_ms=int((time.monotonic() - t0) * 1000),
    )


@app.get("/", include_in_schema=False)
def root():
    return {"message": "MLOps Model Serving Platform. Visit /docs for usage."}
