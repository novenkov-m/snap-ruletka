from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

# Auth
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(BaseModel):
    id: UUID
    email: str
    view_balance: int
    created_at: datetime

    class Config:
        from_attributes = True

# Photo
class PhotoOut(BaseModel):
    id: UUID
    url: str       # подписанный URL
    thumbnail_url: str
    liked_by_me: Optional[bool] = False

class LikeResponse(BaseModel):
    liked: bool