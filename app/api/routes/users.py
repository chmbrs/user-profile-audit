from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import UserData
from app.db.db_funcs import Database
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserData, db: Database = Depends(get_db)):
    user = await db.create_user(name=user_data.name, email=user_data.email)
    return {"message": "User created successfully", "user": user}

@router.get("/")
async def get_users(db: Database = Depends(get_db)):
    users = await db.get_users()
    return {"users": users}

@router.get("/{user_id}")
async def get_user(user_id: int, db: Database = Depends(get_db)):
    user = await db.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"user": user}

@router.put("/{user_id}")
async def update_user(user_id: int, user_data: UserData, db: Database = Depends(get_db)):
    user = await db.update_user(user_id=user_id, name=user_data.name, email=user_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User updated successfully", "user": user}

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Database = Depends(get_db)):
    user = await db.delete_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully", "user": user}
