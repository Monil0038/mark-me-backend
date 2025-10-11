from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.user.models import UserRoles
from utils.schemas.base import BaseSchema


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    image_url: Optional[str] = None

    email: Optional[str] = None
    phone_number_country_code: Optional[str] = None
    phone_number: Optional[str] = None

    department: Optional[str] = None


class UserRequest(UserUpdate):
    firstname: str
    lastname: str
    email: str


class UserResponse(UserUpdate):
    role: str = UserRoles.FACULTY.value
    is_active: bool = True
    is_banned: bool = False

    class Config:
        from_attributes = True


class UserBase(BaseSchema, UserResponse):
    id: Optional[str]
    updated_by: Optional[str]
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    user: UserResponse
    token: str


class FacultyResponse(UserUpdate):
    id: str
    is_active: bool = True
    is_banned: bool = False
    created_at: datetime

    class Config:
        from_attributes = True