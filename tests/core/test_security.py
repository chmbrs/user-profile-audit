import pytest
from fastapi.security import HTTPBasicCredentials
from fastapi import HTTPException
from app.core.security import verify_credentials
from fastapi import status


@pytest.fixture
def mock_valid_settings(monkeypatch):
    monkeypatch.setattr("app.core.config.settings.VALID_USER_NAME", "valid_user_name")
    monkeypatch.setattr("app.core.config.settings.VALID_PASSWORD", "valid_password")

def test_verify_credentials_valid(mock_valid_settings):
    credentials = HTTPBasicCredentials(username="valid_user_name", password="valid_password")

    assert verify_credentials(credentials) is None

def test_verify_credentials_invalid_username(mock_valid_settings):
    credentials = HTTPBasicCredentials(username="invavalid_user_name", password="valid_password")
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(credentials)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid credentials"

def test_verify_credentials_invalid_password(mock_valid_settings):
    credentials = HTTPBasicCredentials(username="valid_user_name", password="invalid_password")
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(credentials)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid credentials"

def test_verify_credentials_invalid_both(mock_valid_settings):
    credentials = HTTPBasicCredentials(username="invalid_user_name", password="invalid_password")
    with pytest.raises(HTTPException) as exc_info:
        verify_credentials(credentials)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid credentials"
