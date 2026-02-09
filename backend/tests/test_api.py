from fastapi.testclient import TestClient
import pytest


@pytest.mark.crud
def test_create_reminder(client: TestClient, reminder_payload):
    """
    Creating reminder, id should appera in data
    """
    response = client.post("/create", json=reminder_payload)

    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Laundry"
    assert "id" in data


@pytest.mark.crud
def test_get_reminder(client: TestClient, reminder_payload):
    """
    Get one reminder, values should be matching
    """
    response = client.post("/create", json=reminder_payload)
    assert response.status_code == 200
    data = response.json()

    response_get = client.get(f"/reminders/{data.get('id')}")

    assert response_get.status_code == 200
    data_get = response_get.json()
    assert data_get['title'] == reminder_payload['title']
    assert data_get['description'] == reminder_payload['description']
    assert data_get['email'] == reminder_payload['email']
    assert data_get['alert_type'] == reminder_payload['alert_type']


@pytest.mark.crud
def test_delete_reminder_and_error(client: TestClient, reminder_payload):
    """
    Tests deleting all reminders.
    Aditionally checks status code for deleting non existing reminder
    """
    response = client.post("/create", json=reminder_payload)
    assert response.status_code == 200
    data = response.json()
    response_delete = client.delete(f"/reminders/{data['id']}")
    assert response_delete.status_code == 200
    response_delete_2 = client.delete(f"/reminders/{data['id']}")
    assert response_delete_2.status_code == 404


@pytest.mark.crud
def test_put(client: TestClient, reminder_payload):
    """
    Tests PUT for Reminder, should return status code 200 and new values
    """
    response = client.post("/create", json=reminder_payload)
    assert response.status_code == 200
    data = response.json()

    payload_put = {
        "title": "Clean windows",
        'description': "I've changed my mind"
    }

    response_put = client.put(f"/reminders/{data['id']}", json=payload_put)
    assert response_put.status_code == 200

    response_get = client.get(f"/reminders/{data['id']}")
    data_get = response_get.json()

    assert data_get['title'] == payload_put["title"]
    assert data_get['description'] == payload_put['description']
    assert data_get['email'] == reminder_payload['email']
    assert data_get['alert_type'] == reminder_payload['alert_type']


@pytest.mark.validation
def test_wrong_date(client: TestClient):
    """
    Tests providing wrong date format, should return status code 422 and ValueError
    """
    payload = {
        "title": 'Laundry',
        "description": "Remember about laundry",
        "due_to": "2026-12-42T12:00Z",
        "email": "test@example.com",
        "alert_type": "minutes"
    }
    response = client.post("/create", json=payload)
    assert response.status_code == 422
    assert "Field should be filled in dd-mm-yyyy hh:mm format" in response.text


@pytest.mark.crud
def test_all_reminders(client: TestClient, reminder_payload):
    """
    Tests if getting all reminders works properly
    """
    response = client.post("/create", json=reminder_payload)
    assert response.status_code == 200
    response2 = client.post("/create", json=reminder_payload)
    assert response2.status_code == 200

    response_get_all = client.get("/reminders")
    assert response_get_all.status_code == 200
    assert len(response_get_all.json()) == 2


@pytest.mark.crud
def test_delete_all(client: TestClient, reminder_payload):
    """
    Test of deleting all reminders, should return empty list after.
    Message returned if trying to delete empty list.
    """
    response = client.post("/create", json=reminder_payload)
    assert response.status_code == 200
    response2 = client.post("/create", json=reminder_payload)
    assert response2.status_code == 200

    response_delete = client.delete("/reminders")
    assert response_delete.status_code == 200

    response_get_all = client.get("/reminders")
    assert response_get_all.status_code == 200
    assert response_get_all.json() == []

    response_delete = client.delete("/reminders")
    assert response_delete.status_code == 200
    assert response_delete.json() == {'message': 'No reminders to delete'}
