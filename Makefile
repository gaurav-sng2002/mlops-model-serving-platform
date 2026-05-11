.PHONY: install test lint format run docker-build docker-up docker-down clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/

lint:
	black --check src/ tests/
	isort --check-only src/ tests/
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

run:
	python -m src.model_serving.main

docker-build:
	docker build -t model-serving:latest -f docker/Dockerfile .

docker-up:
	docker-compose -f docker/docker-compose.yaml up -d

docker-down:
	docker-compose -f docker/docker-compose.yaml down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf dist/ build/ *.egg-info
