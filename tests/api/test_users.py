import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app
from app.db.db_funcs import Database

client = TestClient(app)

@pytest.fixture
def sample_user():
    return {"name": "Lukas Ruiz", "email": "lukasculture@example.com"}

@pytest.fixture
def mock_create_user():
    with patch.object(Database, "create_user") as mock:
        mock.return_value = {
            "id": 1,
            "name": "Lukas Ruiz",
            "email": "lukasculture@example.com",
            "created_at": "2023-11-22T16:28:57.123456+00:00",
            "updated_at": "2023-11-22T16:28:57.123456+00:00",
        }
        yield mock

@pytest.fixture
def mock_get_users():
    with patch.object(Database, "get_users") as mock:
        mock.return_value = [
            {
                "id": 1,
                "name": "Lukas Ruiz",
                "email": "lukasculture@example.com",
                "created_at": "2023-11-22T16:28:57.123456+00:00",
                "updated_at": "2023-11-22T16:28:57.123456+00:00",
            }
        ]
        yield mock

@pytest.fixture
def mock_get_user():
    with patch.object(Database, "get_user") as mock:
        mock.side_effect = lambda user_id: {
            1: {
                "id": 1,
                "name": "Lukas Ruiz",
                "email": "lukasculture@example.com",
                "created_at": "2023-11-22T16:28:57.123456+00:00",
                "updated_at": "2023-11-22T16:28:57.123456+00:00",
            }
        }.get(user_id)
        yield mock

@pytest.fixture
def mock_update_user():
    with patch.object(Database, "update_user") as mock:
        mock.side_effect = lambda user_id, name, email: {
            "id": user_id,
            "name": name,
            "email": email,
            "created_at": "2023-11-22T16:28:57.123456+00:00",
            "updated_at": "2023-11-22T16:28:57.123456+00:00",
        }
        yield mock

@pytest.fixture
def mock_delete_user():
    with patch.object(Database, "delete_user") as mock:
        mock.return_value = {
            "id": 1,
            "name": "Lukas Ruiz",
            "email": "lukasculture@example.com",
            "created_at": "2023-11-22T16:28:57.123456+00:00",
            "updated_at": "2023-11-22T16:28:57.123456+00:00",
        }
        yield mock

@pytest.mark.parametrize(
    "endpoint,method,data,status_code",
    [
        ("/users", client.post, {"name": "Lukas", "email": "test@example.com"}, status.HTTP_201_CREATED),
        ("/users", client.post, {"name": ""}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("/users/1", client.get, None, status.HTTP_200_OK),
        ("/users/2", client.get, None, status.HTTP_404_NOT_FOUND),
    ],
)

def test_user_operations(endpoint, method, data, status_code, mock_create_user, mock_get_user):
    response = method(endpoint, json=data) if data else method(endpoint)
    assert response.status_code == status_code

def test_get_all_users(mock_get_users):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert "users" in response.json()

def test_update_user(mock_update_user):
    updated_data = {"name": "Updated User", "email": "updated@example.com"}
    response = client.put("/users/1", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user"]["name"] == updated_data["name"]

def test_delete_user(mock_delete_user):
    response = client.delete("/users/1")
    assert response.status_code == status.HTTP_200_OK
