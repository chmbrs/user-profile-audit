from app.db.db_funcs import Database

# Create a global database instance
db = Database()

async def get_db() -> Database:  # pragma: no cover
    """
    Dependency function to provide a database connection instance
    to route handlers.
    """
    return db