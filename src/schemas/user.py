import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr
    password: constr(min_length=5)
    username: Optional[constr(min_length=3, max_length=20)] = None


class UserFullInfo(UserBase):
    id: uuid.UUID
    created_at: datetime
    # products: ProductUserInfo
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=5)] = None
    username: Optional[constr(min_length=3, max_length=20)] = None
