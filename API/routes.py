from fastapi import APIRouter
from API.models import CheckHWIDModel

router = APIRouter(prefix="",tags=["Чек лицензии"])

@router.post("/check_hwid")
async def check_hwid(hwid: str) -> CheckHWIDModel:
    return {"ok": True, "user_id": 12124124}