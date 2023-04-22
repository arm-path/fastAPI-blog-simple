from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel
from pydantic import EmailStr


class UserRead(BaseUser):
    id: int
    email: EmailStr
    role_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(BaseUserCreate):
    email: EmailStr
    password: str
    role_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseUserUpdate):
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: Optional[int]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class RoleCreate(BaseModel):
    title: str
