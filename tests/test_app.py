import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_for_activity():
    activity = "Basketball Team"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_unregister_participant():
    activity = "Basketball Team"
    email = "testuser@mergington.edu"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Try unregistering again (should fail)
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]
