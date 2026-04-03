import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Create a test client
client = TestClient(app)

# Initial activities copy for resetting
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for tournament play",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis skills development and friendly matches",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["marcus@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and mixed media art creation",
        "schedule": "Wednesdays and Saturdays, 2:00 PM - 4:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "grace@mergington.edu"]
    },
    "Music Band": {
        "description": "Join our jazz and rock band performances",
        "schedule": "Mondays and Fridays, 3:00 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ryan@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science competitions and experiments",
        "schedule": "Tuesdays and Saturdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["noah@mergington.edu", "chloe@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    global activities
    activities.clear()
    activities.update(initial_activities)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Number of activities
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]
    # Check if added to participants
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_for_activity_duplicate():
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
    # Second signup should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]

def test_remove_participant_success():
    response = client.delete("/activities/Chess%20Club/participants/michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Removed michael@mergington.edu from Chess Club" in data["message"]
    # Check if removed
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

def test_remove_participant_not_found():
    response = client.delete("/activities/Chess%20Club/participants/nonexistent@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Participant not registered for this activity" in data["detail"]

def test_remove_participant_activity_not_found():
    response = client.delete("/activities/Nonexistent%20Activity/participants/michael@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]