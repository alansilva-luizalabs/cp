from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(monkeypatch):
    """Provide an isolated TestClient with reset in-memory activities."""
    baseline_activities = deepcopy(app_module.activities)
    monkeypatch.setattr(app_module, "activities", deepcopy(baseline_activities))
    return TestClient(app_module.app)
