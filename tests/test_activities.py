"""Tests for GET /activities endpoint"""

def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have activities
    assert len(activities) > 0
    
    # Expected activity names
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    ]
    
    for activity_name in expected_activities:
        assert activity_name in activities


def test_activity_has_required_fields(client):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_activity_participants_is_list(client):
    """Test that participants field is a list"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants should be a list"
        
        # All participants should be strings (emails)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str), \
                f"Activity '{activity_name}' has non-string participant"


def test_activity_max_participants_is_integer(client):
    """Test that max_participants is an integer"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"Activity '{activity_name}' max_participants should be an integer"
