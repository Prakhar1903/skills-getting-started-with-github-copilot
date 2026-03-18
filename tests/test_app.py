from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def reset_participants():
    # Reset single-run modifications to keep tests idempotent
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]


def test_get_activities():
    reset_participants()
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    reset_participants()
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_fails():
    reset_participants()
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400


def test_remove_participant():
    reset_participants()
    email = "michael@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_remove_participant_not_found():
    reset_participants()
    response = client.delete("/activities/Chess Club/participants", params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404
