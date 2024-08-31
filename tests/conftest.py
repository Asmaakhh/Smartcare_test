import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mongo_mock(monkeypatch):
    # Ensure the correct path is used here
    from app.utils.mongo import mongo

    mongo_mock = MagicMock()

    # Patch the MongoDB client in your app to use this mock
    monkeypatch.setattr("app.utils.mongo.mongo", mongo_mock)

    return mongo_mock
