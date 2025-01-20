from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from contextlib import asynccontextmanager

from httpx import Request

import config
from app.models.user import UserData
from app.db.db_funcs import Database

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI): # pragma: no cover
    await db.connect()
    customize_openapi(app)
    try:
        yield
    finally:
        await db.disconnect()

app = FastAPI(lifespan=lifespan)
security = HTTPBasic()

async def get_db(): # pragma: no cover
    return db

def verify_credentials(credentials: HTTPBasicCredentials):
    valid_username = config.VALID_USER_NAME
    valid_password = config.VALID_PASSWORD
    if credentials.username != valid_username or credentials.password != valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

def customize_openapi(app: FastAPI):
    """Customize OpenAPI schema to include BasicAuth security scheme."""
    if app.openapi_schema:
        return

    openapi_schema = app.openapi()
    openapi_schema["components"]["securitySchemes"] = {
        "BasicAuth": {
            "type": "http",
            "scheme": "basic",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BasicAuth": []}])
    app.openapi_schema = openapi_schema

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path not in ["/docs", "/openapi.json"]:  # Exclude Swagger docs
        credentials = await security(request)
        verify_credentials(credentials)
    return await call_next(request)

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
