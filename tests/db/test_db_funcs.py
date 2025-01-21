import pytest
from unittest.mock import AsyncMock

from app.db.db_funcs import Database

# This test needs the actual connection with the db to function and to have a user in it
#async def test_create_user():
#    db = Database()
#    await db.connect()
#    user = await db.get_user(user_id=1)
#    assert user["name"] == "John Doe"
#    assert user["email"] == "john@example.com"
#    await db.disconnect()

@pytest.fixture
def mock_database():
    db = Database()
    db.pool = AsyncMock()  # Mock the connection pool
    return db

@pytest.mark.asyncio
async def test_create_user(mock_database):
    mock_database.fetchrow = AsyncMock(return_value={"id": 1, "name": "Test User", "email": "test@example.com"})
    mock_database.execute = AsyncMock()

    user = await mock_database.create_user("Test User", "test@example.com")

    assert user["id"] == 1
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"

    mock_database.fetchrow.assert_awaited_once()
    mock_database.execute.assert_awaited_once_with(
        """
        INSERT INTO user_audit (user_id, operation, name, email, deleted)
        VALUES ($1, $2, $3, $4, $5);
        """,
        1, "CREATE", "Test User", "test@example.com", False
    )

@pytest.mark.asyncio
async def test_get_user(mock_database):
    mock_database.fetchrow = AsyncMock(return_value={"id": 1, "name": "Test User", "email": "test@example.com"})

    user = await mock_database.get_user(1)

    assert user["id"] == 1
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"

    mock_database.fetchrow.assert_awaited_once

@pytest.mark.asyncio
async def test_get_users(mock_database):
    mock_database.fetch = AsyncMock(return_value=[
        {"id": 1, "name": "User1", "email": "user1@example.com"},
        {"id": 2, "name": "User2", "email": "user2@example.com"}
    ])

    users = await mock_database.get_users()

    assert len(users) == 2
    assert users[0]["name"] == "User1"

    mock_database.fetch.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_user(mock_database):
    mock_database.fetchrow = AsyncMock(return_value={"id": 1, "name": "Updated User", "email": "updated@example.com"})
    mock_database.execute = AsyncMock()

    user = await mock_database.update_user(1, "Updated User", "updated@example.com")

    assert user["name"] == "Updated User"
    assert user["email"] == "updated@example.com"

    mock_database.fetchrow.assert_awaited_once()
    mock_database.execute.assert_awaited_once_with(
        """
        INSERT INTO user_audit (user_id, operation, name, email, deleted)
        VALUES ($1, $2, $3, $4, $5);
        """,
        1, "UPDATE", "Updated User", "updated@example.com", False
    )

@pytest.mark.asyncio
async def test_delete_user(mock_database):
    mock_database.fetchrow = AsyncMock(return_value={"id": 1, "name": "Test User", "email": "deleted_1", "deleted": True})
    mock_database.execute = AsyncMock()

    user = await mock_database.delete_user(1)

    assert user["email"] == "deleted_1"
    assert user["deleted"] is True

    mock_database.fetchrow.assert_awaited_once()
    mock_database.execute.assert_awaited_once_with(
        """
        INSERT INTO user_audit (user_id, operation, name, email, deleted)
        VALUES ($1, $2, $3, $4, $5);
        """,
        1, "DELETE", "Test User", "deleted_1", True
    )
