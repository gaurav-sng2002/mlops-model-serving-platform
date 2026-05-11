FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml .
# Install basic dependencies (not all, just enough for builder context if needed)
# In this multi-stage, we'll install directly to the final image for simplicity
# due to the heavy ML dependencies

FROM python:3.10-slim

# Install runtime dependencies including libgomp for XGBoost/LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir hatchling
# Install all dependencies without the dev group
RUN pip install --no-cache-dir .

# Copy source code
COPY src/ /app/src/

# Set Python path
ENV PYTHONPATH=/app/src
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "src.model_serving.main"]
