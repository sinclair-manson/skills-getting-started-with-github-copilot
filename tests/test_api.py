from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]


def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=dup@mergington.edu")
    # Second attempt
    response = client.post("/activities/Programming%20Class/signup?email=dup@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_delete_success():
    # Signup first
    client.post("/activities/Gym%20Class/signup?email=del@mergington.edu")
    # Then delete
    response = client.delete("/activities/Gym%20Class/signup?email=del@mergington.edu")
    assert response.status_code == 200
    result = response.json()
    assert "Removed" in result["message"]


def test_delete_not_signed_up():
    response = client.delete("/activities/Basketball/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]


def test_delete_invalid_activity():
    response = client.delete("/activities/Invalid/signup?email=test@mergington.edu")
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert "/static/index.html" in response.headers["location"]