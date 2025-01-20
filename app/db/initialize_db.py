import os
import asyncio
from asyncpg import create_pool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL
);
"""

CREATE_USERS_AUDIT_TABLE = """
CREATE TABLE IF NOT EXISTS user_audit (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    operation VARCHAR(50) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255),
    deleted BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

async def init_db():  # pragma: no cover
    pool = await create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        print("Initializing the database...")
        await conn.execute(CREATE_USERS_TABLE)
        await conn.execute(CREATE_USERS_AUDIT_TABLE)
        print("Database initialized successfully.")
    await pool.close()

if __name__ == "__main__":
    asyncio.run(init_db())
