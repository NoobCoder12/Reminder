from fastapi.testclient import TestClient
from app.main import get_db


def test_create_reminder(client: TestClient):
    payload = {
        "title": 'Laundry',
        "description": "Remember about laundry",
        "due_to": "24-12-2026 12:00",
        "email": "test@example",
        "alert_type": "minutes"
    }

    response = client.post("/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Laundry"
    assert "id" in data
