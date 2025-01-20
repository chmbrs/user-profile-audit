from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.openapi import customize_openapi
from app.api.dependencies import db
from app.api.routes import health, users, audit, restore

@asynccontextmanager
async def lifespan(app: FastAPI):  # pragma: no cover
    await db.connect()
    customize_openapi(app)
    try:
        yield
    finally:
        await db.disconnect()

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.include_router(health.router, prefix="/health", tags=["Health Check"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(audit.router, prefix="/audit", tags=["Audit"])
app.include_router(restore.router, prefix="/restore", tags=["Restore"])
