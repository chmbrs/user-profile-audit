from fastapi import APIRouter, Depends
from app.db.db_funcs import Database
from app.api.dependencies import get_db

router = APIRouter()

@router.get("/")
async def get_audit_logs(db: Database = Depends(get_db)):
    logs = await db.get_audit_logs()
    return {"audit_logs": logs}
