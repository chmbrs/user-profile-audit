from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse

class UserData(BaseModel):
    name: str
    email: str

app = FastAPI()

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
