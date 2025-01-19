from fastapi import FastAPI, status, HTTPException, Depends
from contextlib import asynccontextmanager

from app.models.user import UserData
from app.db.operations import Database

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    try:
        yield
    finally:
        await db.disconnect()

app = FastAPI(lifespan=lifespan)

async def get_db():
    return db

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserData, db: Database = Depends(get_db)):
    try:
        user = await db.create_user(name=user_data.name, email=user_data.email)
        return {"message": "User created successfully", "id": user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {str(e)}")

@app.get("/users")
async def get_users(db: Database = Depends(get_db)):
    users = await db.get_users()
    return {"users": users}


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Database = Depends(get_db)):
    user = await db.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": user}


@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: UserData, db: Database = Depends(get_db)):
    user = await db.update_user(user_id=user_id, name=user_data.name, email=user_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User updated successfully", "user": user}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Database = Depends(get_db)):
    user = await db.delete_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully", "user": user}