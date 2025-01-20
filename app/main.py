from fastapi import FastAPI, status, HTTPException, Depends
from contextlib import asynccontextmanager

from app.models.user import UserData
from app.db.db_funcs import Database

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI): # pragma: no cover
    await db.connect()
    try:
        yield
    finally:
        await db.disconnect()

app = FastAPI(lifespan=lifespan)

async def get_db(): # pragma: no cover
    return db

@app.get("/health")
async def health_check(): # pragma: no cover
    return {"status": "ok"}

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserData, db: Database = Depends(get_db)):
    try:
        user = await db.create_user(name=user_data.name, email=user_data.email)
        return {"message": "User created successfully", "user": user}
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

@app.get("/audit")
async def get_audit_logs(db: Database = Depends(get_db)):
    logs = await db.get_audit_logs()
    return {"audit_logs": logs}

@app.post("/users/{user_id}/restore")
async def restore_user(user_id: int, version: int, db: Database = Depends(get_db)):
    audit_log = await db.get_user_audit_restore_version(user_id, version)
    if not audit_log:
        raise HTTPException(status_code=404, detail="Version not found for restoration.")

    restored_user = await db.restore_user(user_id, audit_log["name"], audit_log["email"], audit_log["deleted"])
    if not restored_user:
        raise HTTPException(status_code=404, detail="User not found for restoration.")

    return {"restored_user": restored_user}
