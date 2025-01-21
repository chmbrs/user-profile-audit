import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.db.db_funcs import Database

client = TestClient(app)

@pytest.fixture
def mock_get_audit_logs():
    with patch.object(Database, "get_audit_logs") as mock:
        mock.return_value = [
            {
                "user_id": 1,
                "name": "Lukas Ruiz",
                "email": "lukasculture@example.com",
                "deleted": False,
                "version": 1,
            }
        ]
        yield mock


def test_get_audit_logs(mock_get_audit_logs):
    response = client.get("/audit")
    assert response.status_code == status.HTTP_200_OK
    assert "audit_logs" in response.json()
