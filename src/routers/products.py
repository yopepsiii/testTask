import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.cruds.products import get_products, create_product, delete_product, get_product, update_product
from src.db import models
from src.db.db import get_db
from src.oauth import get_current_user
from src.schemas.auth import TokenData
from src.schemas.product import ProductCreate, ProductPreview, ProductFull, ProductUpdate

router = APIRouter(prefix="/products", tags=["Продукты"])


@router.get("/", response_model=list[ProductPreview])
async def get_products_endpoint(db: AsyncSession = Depends(get_db),
                                limit: int = 10,
                                page: int = 1,
                                search: Optional[str] = "",
                                category_id: Optional[int] = None,
                                current_user_data: TokenData = Depends(get_current_user)):
    return await get_products(db, limit, page, category_id, search)


@router.get("/{product_id}", response_model=ProductFull)
async def get_product_endpoint(product_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                               current_user_data: TokenData = Depends(get_current_user)):
    return await get_product(db, product_id)


@router.post("/", response_model=ProductFull, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(new_product_json: ProductCreate,
                                  db: AsyncSession = Depends(get_db),
                                  current_user_data: TokenData = Depends(get_current_user)):
    return await create_product(db, new_product_json, uuid.UUID(current_user_data.user_id))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                                  current_user_data: TokenData = Depends(get_current_user)):
    return await delete_product(db, product_id)


@router.patch("/{product_id}", response_model=ProductFull)
async def update_product_endpoint(product_id: uuid.UUID, update_product_json: ProductUpdate,
                                  db: AsyncSession = Depends(get_db),
                                  current_user_data: TokenData = Depends(get_current_user)):
    return await update_product(db, product_id, uuid.UUID(current_user_data.user_id), update_product_json)
