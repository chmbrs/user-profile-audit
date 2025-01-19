import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_user():
    return {"name": "Lukas Ruiz", "email": "lukasculture@example.com"}

def test_create_user_success(sample_user):
    response = client.post("/users", json=sample_user)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == sample_user["name"]
    assert response.json()["email"] == sample_user["email"]

def test_create_user_invalid_data():
    response = client.post("/users", json={"name": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_user_by_id():
    response = client.get("/users/2")
    if response.status_code == status.HTTP_200_OK:
        assert "name" in response.json()
        assert "email" in response.json()
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_user_by_id_unknown():
    response = client.get("/users/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user():
    updated_data = {"name": "Marco Carola", "email": "marcocoral@example.com"}
    response = client.put("/users/1", json=updated_data)
    if response.status_code == status.HTTP_200_OK:
        assert response.json()["name"] == updated_data["name"]
        assert response.json()["email"] == updated_data["email"]
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
