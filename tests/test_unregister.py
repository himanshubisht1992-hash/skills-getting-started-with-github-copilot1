"""
Tests for unregister endpoints following the AAA (Arrange-Act-Assert) pattern.
"""


def test_unregister_participant_success(client):
    """Test successfully unregistering a participant from an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "unregister@mergington.edu"
    
    # Sign up first
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert email in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_removes_participant_from_list(client):
    """Test that unregister properly removes participant from activity."""
    # Arrange
    activity_name = "Gym Class"
    email = "remove@mergington.edu"
    
    # Sign up first
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act
    client.delete(f"/activities/{activity_name}/signup?email={email}")
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert email not in activities[activity_name]["participants"]


def test_unregister_non_existent_participant_fails(client):
    """Test that unregistering a non-registered student fails."""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    error_detail = response.json()["detail"]
    
    # Assert
    assert response.status_code == 404
    assert "not signed up" in error_detail


def test_unregister_invalid_activity_not_found(client):
    """Test that unregister fails for non-existent activity."""
    # Arrange
    invalid_activity = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
