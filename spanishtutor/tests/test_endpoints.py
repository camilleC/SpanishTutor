# --- FastAPI endpoint tests ---
from fastapi.testclient import TestClient
from spanishtutor.src.api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_valid():
    payload = {"message": "A1", "history": []}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert "reply" in response.json()

def test_chat_invalid_payload():
    # Missing 'message' field
    payload = {"history": []}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422

    # Wrong type for history
    payload = {"message": "A1", "history": "notalist"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 422

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"chat_turns_total" in response.content 

def test_invalid_endpoint():
    response = client.get("/bad")
    assert response.status_code == 404
