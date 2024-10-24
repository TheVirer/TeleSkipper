from pydantic import BaseModel

class CheckHWIDModel(BaseModel):
    ok: bool = True
    user_id: int

class GetUserModel(BaseModel):
    name: str
    config: dict