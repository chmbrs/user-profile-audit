import asyncpg
from config import DATABASE_URL

class Database:
    def __init__(self): # pragma: no cover
        self.pool = None

    async def connect(self): # pragma: no cover
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            print("Connected to database successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    async def disconnect(self): # pragma: no cover
        await self.pool.close()

    async def execute(self, query, *args): # pragma: no cover
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query, *args): # pragma: no cover
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query, *args): # pragma: no cover
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def log_audit(self, user_id, operation, deleted, name=None, email=None):
        query = """
        INSERT INTO user_audit (user_id, operation, name, email, deleted)
        VALUES ($1, $2, $3, $4, $5);
        """
        await self.execute(query, user_id, operation, name, email, deleted)

    async def create_user(self, name: str, email: str):
        query = """
        INSERT INTO users (name, email, deleted)
        VALUES ($1, $2, false)
        RETURNING id, name, email;
        """
        user = await self.fetchrow(query, name, email)
        await self.log_audit(user["id"], "CREATE", False, name, email)
        return user

    async def get_user(self, user_id: int):
        query = "SELECT id, name, email, created_at, updated_at FROM users WHERE id = $1 AND deleted = false;"
        return await self.fetchrow(query, user_id)

    async def get_users(self):
        query = "SELECT id, name, email, created_at, updated_at FROM users WHERE deleted = false;"
        return await self.fetch(query)

    async def update_user(self, user_id: int, name: str, email: str):
        query = """
            UPDATE users
            SET name = $1, email = $2, updated_at = CURRENT_TIMESTAMP
            WHERE id = $3 AND deleted = false
            RETURNING id, name, email;
        """
        user = await self.fetchrow(query, name, email, user_id)
        if user:
            await self.log_audit(user_id, "UPDATE", False, name, email)
        return user

    async def delete_user(self, user_id: int):
        query = "UPDATE users SET deleted = true WHERE id = $1 RETURNING id, name, email, deleted;"
        user = await self.fetchrow(query, user_id)
        if user:
            await self.log_audit(user_id, "DELETE", True, user['name'], user['email'])
        return user

    async def get_audit_logs(self):
        query = "SELECT * FROM user_audit ORDER BY timestamp DESC;"
        return await self.fetch(query)

    async def get_user_audit_restore_version(self, user_id: int, version: int):
        query = """
            SELECT * FROM user_audit
            WHERE user_id = $1
            ORDER BY id ASC
            LIMIT 1 OFFSET $2;
            """
        return await self.fetchrow(query, user_id, version - 1)

    async def restore_user(self, user_id: int, name, email, deleted):
        restore_query = """
            UPDATE users
            SET name = $2, email = $3, updated_at = CURRENT_TIMESTAMP, deleted = $4
            WHERE id = $1
            RETURNING id, name, email;
        """
        restored_user =  await self.fetchrow(restore_query, user_id, name, email, deleted)

        if restored_user:
            await self.log_audit(user_id, "RESTORE", deleted, name, email)

        return  restored_user
