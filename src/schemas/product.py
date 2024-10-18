import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.db.models import Category
from src.schemas.category import CategoryOut


class ProductBase(BaseModel):
    title: str
    description: str
    price: float


class ProductCreate(ProductBase):
    category_id: int
    width: int
    height: int


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None


class ProductPreview(ProductBase):
    id: uuid.UUID
    pass


class ProductFull(ProductBase):
    id: uuid.UUID
    width: int
    height: int
    category: CategoryOut

    class Config:
        from_attributes = True
