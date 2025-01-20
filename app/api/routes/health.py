from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check(): # pragma: no cover
    return {"status": "ok"}