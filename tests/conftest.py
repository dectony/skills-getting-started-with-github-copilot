import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def original_activities_snapshot():
    return copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(original_activities_snapshot):
    activities.clear()
    activities.update(copy.deepcopy(original_activities_snapshot))
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_activities_snapshot))


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
