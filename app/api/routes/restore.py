from fastapi import APIRouter, Depends, HTTPException
from app.db.db_funcs import Database
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/{user_id}")
async def restore_user(user_id: int, version: int, db: Database = Depends(get_db)):
    audit_log = await db.get_user_audit_restore_version(user_id, version)
    if not audit_log:
        raise HTTPException(status_code=404, detail="Version not found for restoration.")
    restored_user = await db.restore_user(user_id, audit_log["name"], audit_log["email"], audit_log["deleted"])
    return {"restored_user": restored_user}
