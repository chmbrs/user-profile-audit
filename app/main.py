from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.models.user import UserData
from app.db.main import Database

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    await db.connect()
    yield
    # Shutdown actions
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

# Placeholder routes for testing
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserData):
    return {"name": user_data.name, "email": user_data.email}

@app.get("/users")
async def get_users():
    return []

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id == 1:
        return {"name": "", "email": ""}
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserData):
    return user_data

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return {"message": f"Delete user with ID {user_id} (placeholder)"}
