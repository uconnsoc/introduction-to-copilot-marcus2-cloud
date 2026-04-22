"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


def test_signup_successfully_registers_student(client):
    """Test that a student can successfully sign up for an activity"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found_returns_404(client):
    """Test that signing up for non-existent activity returns 404"""
    response = client.post(
        "/activities/NonexistentActivity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_registration_returns_400(client):
    """Test that registering the same student twice returns 400"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # First signup (already exists, should fail)
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_different_students_same_activity(client):
    """Test that multiple different students can sign up for the same activity"""
    activity_name = "Programming Class"
    student1 = "alice@mergington.edu"
    student2 = "bob@mergington.edu"
    
    # First student signs up
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student1}
    )
    assert response1.status_code == 200
    
    # Second student signs up
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": student2}
    )
    assert response2.status_code == 200
    
    # Verify both are registered
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participants = activities[activity_name]["participants"]
    
    assert student1 in participants
    assert student2 in participants


def test_signup_same_student_different_activities(client):
    """Test that the same student can sign up for multiple different activities"""
    email = "flexible@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Drama Club"
    
    # Sign up for first activity
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    # Verify registered in both
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    assert email in activities[activity1]["participants"]
    assert email in activities[activity2]["participants"]


def test_signup_increments_participant_count(client):
    """Test that signup increments the participant count"""
    activity_name = "Art Club"
    email = "artist@mergington.edu"
    
    # Get initial participant count
    response_before = client.get("/activities")
    activities_before = response_before.json()
    initial_count = len(activities_before[activity_name]["participants"])
    
    # Sign up
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Get updated participant count
    response_after = client.get("/activities")
    activities_after = response_after.json()
    final_count = len(activities_after[activity_name]["participants"])
    
    assert final_count == initial_count + 1
