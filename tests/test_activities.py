"""
Tests for activity endpoints following the AAA (Arrange-Act-Assert) pattern.
"""


def test_get_root(client):
    """Test that the root endpoint redirects to static/index.html."""
    # Arrange
    expected_redirect = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect


def test_get_activities(client):
    """Test retrieving all activities returns proper structure."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(activities, dict)
    assert len(activities) > 0
    for activity_name, activity in activities.items():
        assert all(field in activity for field in required_fields)
        assert isinstance(activity["participants"], list)


def test_get_activities_participant_counts_valid(client):
    """Test that participant counts don't exceed max capacity."""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity in activities.items():
        participants_count = len(activity["participants"])
        max_participants = activity["max_participants"]
        assert participants_count <= max_participants, \
            f"{activity_name} exceeds capacity: {participants_count}/{max_participants}"
