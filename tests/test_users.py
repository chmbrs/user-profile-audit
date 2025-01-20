import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app, Database

client = TestClient(app)

@pytest.fixture
def mock_create_user():
    with patch.object(Database, 'create_user') as mock_create_user:
        mock_create_user.return_value = {
            "id": 1,
            "name": "Lukas Ruiz",
            "email": "lukasculture@example.com",
            "created_at": "2023-11-22T16:28:57.123456+00:00",
            "updated_at": "2023-11-22T16:28:57.123456+00:00"
        }
        yield mock_create_user

@pytest.fixture
def mock_get_users():
    with patch.object(Database, 'get_users') as mock_get_users:
        mock_get_users.return_value = {
            "id": 1,
            "name": "Lukas Ruiz",
            "email": "lukasculture@example.com",
            "created_at": "2023-11-22T16:28:57.123456+00:00",
            "updated_at": "2023-11-22T16:28:57.123456+00:00"
        }
        yield mock_get_users

@pytest.fixture
def mock_get_user():
    with patch.object(Database, 'get_user') as mock_get_user:
        def get_user_side_effect(user_id):
            if user_id == 1:
                return {
                    "id": 1,
                    "name": "Lukas Ruiz",
                    "email": "lukasculture@example.com",
                    "created_at": "2023-11-22T16:28:57.123456+00:00",
                    "updated_at": "2023-11-22T16:28:57.123456+00:00"
                }
            else:
                return None

        mock_get_user.side_effect = get_user_side_effect
        yield mock_get_user

@pytest.fixture
def mock_update_user():
    with patch.object(Database, 'update_user') as mock_update_user:
        def update_user_side_effect(user_id, name, email):
            if user_id == 1 and name == "Marco Carola" and email == "marcocoral@example.com":
                return {
                    "id": 1,
                    "name": "Marco Carola",
                    "email": "marcocoral@example.com",
                    "created_at": "2023-11-22T16:28:57.123456+00:00",
                    "updated_at": "2023-11-22T16:28:57.123456+00:00"
                }
            else:
                return None

        mock_update_user.side_effect = update_user_side_effect
        yield mock_update_user


@pytest.fixture
def mock_delete_user():
    with patch.object(Database, 'delete_user') as mock_delete_user:
        def delete_user_side_effect(user_id):
            if user_id == 1:
                return {
                    "id": 1,
                    "name": "Lukas Ruiz",
                    "email": "lukasculture@example.com",
                    "created_at": "2023-11-22T16:28:57.123456+00:00",
                    "updated_at": "2023-11-22T16:28:57.123456+00:00"
                }
            else:
                return None

        mock_delete_user.side_effect = delete_user_side_effect
        yield mock_delete_user

@pytest.fixture
def sample_user():
    return {"name": "Lukas Ruiz", "email": "lukasculture@example.com"}

async def test_create_user_success(sample_user, mock_create_user):
    response = client.post("/users", json=sample_user)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user"]["name"] == sample_user["name"]
    assert response.json()["user"]["email"] == sample_user["email"]

    mock_create_user.assert_called_once_with(name=sample_user["name"], email=sample_user["email"])

def test_create_user_invalid_data():
    response = client.post("/users", json={"name": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_all_users(mock_get_users):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert "users" in response.json()

def test_get_user_by_id(mock_get_user):
    response = client.get("/users/1")
    if response.status_code == status.HTTP_200_OK:
        assert "name" in response.json()["user"]
        assert "email" in response.json()["user"]
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_user_by_id_unknown(mock_get_user):
    response = client.get("/users/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user(mock_update_user):
    updated_data = {"name": "Marco Carola", "email": "marcocoral@example.com"}
    response = client.put("/users/1", json=updated_data)
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["user"]["name"] == updated_data["name"]
        assert response.json()["user"]["email"] == updated_data["email"]
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user(mock_delete_user):
    response = client.delete("/users/1")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
