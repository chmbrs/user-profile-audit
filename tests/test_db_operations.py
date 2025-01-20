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
