from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_create_and_read_sub():
    payload = {"name": "Netflix", "cost": 1000.0, "category": "video"}
    post_resp = client.post("/subscriptions/", json=payload)
    assert post_resp.status_code == 201
    
    sub_id = post_resp.json()["id"]
    get_resp = client.get(f"/subscriptions/{sub_id}")
    
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Netflix"
    assert get_resp.json()["cost"] == 1000.0

def test_not_found():
    resp = client.get("/subscriptions/999")
    assert resp.status_code == 404
