from prometheus_client import Counter, Histogram, Gauge

# Application Metrics
HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

HTTP_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

# Model Metrics
PREDICTION_COUNT = Counter(
    "model_prediction_total",
    "Total model predictions",
    ["model", "version", "status"]
)

PREDICTION_TIME = Histogram(
    "model_prediction_duration_seconds",
    "Model prediction latency",
    ["model", "version"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

BATCH_SIZE = Histogram(
    "model_prediction_batch_size",
    "Size of prediction batches",
    buckets=[1, 2, 4, 8, 16, 32, 64]
)

MODEL_LOADED = Gauge(
    "model_loaded",
    "Whether a model is loaded (1) or not (0)",
    ["model", "version"]
)
