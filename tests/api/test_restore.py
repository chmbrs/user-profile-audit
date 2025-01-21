import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.db.db_funcs import Database

client = TestClient(app)


@pytest.fixture
def mock_restore_user():
    with patch.object(Database, 'get_user_audit_restore_version') as mock_get_version, \
         patch.object(Database, 'restore_user') as mock_restore_user:
        mock_get_version.return_value = {
            "id": 1,
            "name": "Restored User",
            "email": "restoreduser@example.com",
            "deleted": False,
        }
        mock_restore_user.return_value = {
            "id": 1,
            "name": "Restored User",
            "email": "restoreduser@example.com",
            "deleted": False,
        }
        yield mock_restore_user


def test_restore_user(mock_restore_user):
    response = client.post("restore/1?version=1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["restored_user"]["name"] == "Restored User"
