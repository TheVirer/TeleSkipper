from fastapi import APIRouter
from API.models import CheckHWIDModel, GetUserModel

router = APIRouter(prefix="",tags=["Чек лицензии"])

@router.post("/check_hwid")
async def check_hwid(hwid: str) -> CheckHWIDModel:
    return {"ok": True, "user_id": 12124124}

@router.get("/get_user")
async def get_user(user_id: int) -> GetUserModel:
    return {"name": "ojgwejgo", "config": {}}