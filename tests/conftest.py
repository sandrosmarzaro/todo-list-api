import pytest
from fastapi.testclient import TestClient

from todo_list_api.app import app


@pytest.fixture
def client():
    return TestClient(app)
