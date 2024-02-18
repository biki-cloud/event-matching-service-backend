from fastapi.testclient import TestClient
from main import app
from uuid import uuid4


client = TestClient(app)

def test_hello():
    response = client.get(
        "/hello",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["hello"] == "world"

