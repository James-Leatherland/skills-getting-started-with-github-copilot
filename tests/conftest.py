from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities_state():
    """Keep in-memory activity data deterministic across tests."""
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def sample_activity_name():
    return "Chess Club"


@pytest.fixture
def sample_email():
    return "new.student@mergington.edu"
