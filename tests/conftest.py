"""Pytest configuration and fixtures for FastAPI backend tests"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities database before each test to avoid cross-test contamination"""
    # Store original activities
    original_activities = deepcopy(activities)
    
    yield
    
    # Restore original activities after the test
    activities.clear()
    activities.update(original_activities)
