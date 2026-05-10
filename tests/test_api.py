from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert r.json()["model_loaded"] is True


def test_metrics_endpoint():
    r = client.get("/metrics")
    assert r.status_code == 200
    assert b"predict_requests_total" in r.content


def test_predict_iris():
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "label" in data
    assert 0.0 <= data["confidence"] <= 1.0


def test_predict_versicolor():
    r = client.post("/predict", json={"features": [6.0, 2.9, 4.5, 1.5]})
    assert r.status_code == 200
    assert r.json()["label"] in ("setosa", "versicolor", "virginica")


def test_predict_empty_features():
    r = client.post("/predict", json={"features": []})
    assert r.status_code in (422, 500)
