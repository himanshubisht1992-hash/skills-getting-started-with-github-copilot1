"""
Tests for signup endpoints following the AAA (Arrange-Act-Assert) pattern.
"""


def test_signup_for_activity_success(client):
    """Test successfully signing up a student for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_duplicate_student_rejected(client):
    """Test that duplicate signup attempts are rejected."""
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"
    
    # Act - First signup
    response1 = client.post(f"/activities/{activity_name}/signup?email={email}")
    first_status = response1.status_code
    
    # Act - Duplicate signup
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_status = response2.status_code
    error_detail = response2.json()["detail"].lower()
    
    # Assert
    assert first_status == 200
    assert second_status == 400
    assert "already signed up" in error_detail


def test_signup_invalid_activity_not_found(client):
    """Test that signup fails for non-existent activity."""
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_updates_activity_participants(client):
    """Test that signup properly adds participant to activity's list."""
    # Arrange
    activity_name = "Programming Class"
    email = "verify@mergington.edu"
    
    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert email in activities[activity_name]["participants"]
