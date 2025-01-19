import asyncpg
from config import DATABASE_URL

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    async def disconnect(self):
        await self.pool.close()

    async def execute(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def create_user(self, name: str, email: str):
        query = """
        INSERT INTO users (name, email)
        VALUES ($1, $2)
        RETURNING id, name, email, created_at, updated_at;
        """
        return await self.fetchrow(query, name, email)

    async def get_user(self, user_id: int):
        query = "SELECT * FROM users WHERE id = $1;"
        return await self.fetchrow(query, user_id)

    async def get_users(self):
        query = "SELECT * FROM users;"
        return await self.fetch(query)

    async def update_user(self, user_id: int, name: str, email: str):
        query = """
        UPDATE users
        SET name = $1, email = $2, updated_at = CURRENT_TIMESTAMP
        WHERE id = $3
        RETURNING id, name, email, created_at, updated_at;
        """
        return await self.fetchrow(query, name, email, user_id)

    async def delete_user(self, user_id: int):
        query = "DELETE FROM users WHERE id = $1 RETURNING id;"
        return await self.fetchrow(query, user_id)