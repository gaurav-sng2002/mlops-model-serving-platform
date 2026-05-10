.PHONY: install dev test docker-build docker-run docker-down k8s-apply

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -v --tb=short

docker-build:
	docker build -t mlops-serving:latest .

docker-run:
	docker run -d --name mlops-api -p 8000:8000 mlops-serving:latest

docker-down:
	docker stop mlops-api && docker rm mlops-api

k8s-apply:
	kubectl apply -f k8s/
