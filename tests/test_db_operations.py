import pytest
from unittest.mock import patch, AsyncMock

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
def mock_asyncpg_create_pool():
    with patch('asyncpg.create_pool') as mock_create_pool:
        mock_create_pool.return_value = AsyncMock()  # Create an asynchronous mock for the pool
        yield mock_create_pool

@pytest.fixture
async def db(mock_asyncpg_create_pool):
    db_instance = Database()
    yield db_instance
    await db_instance.disconnect()

async def test_execute(db, mock_asyncpg_create_pool):
    await db.connect()
    await db.execute('SELECT 1')
    mock_asyncpg_create_pool.return_value.acquire.assert_awaited()
    mock_asyncpg_create_pool.return_value.acquire.return_value.__aenter__.return_value.execute.assert_awaited_once()
