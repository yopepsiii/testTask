import uuid

from fastapi import HTTPException
from starlette import status

from src.db import models
from src.schemas.product import ProductCreate, ProductUpdate

from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


async def get_products(
        db: AsyncSession,
        limit: int,
        page: int,
        category_id: Optional[int] = None,
        search: Optional[str] = None
):
    offset = (page - 1) * limit

    query = select(models.Product)

    if search:
        query = query.where(
            or_(
                models.Product.title.ilike(f"%{search}%"),
                models.Product.description.ilike(f"%{search}%")
            )
        )

    if category_id:
        print(category_id)
        query = query.filter(models.Product.category_id == category_id)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)

    products = result.scalars().all()
    return products


async def get_product(db: AsyncSession, product_id: uuid.UUID):
    product = await db.get(models.Product, product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Продукт с ID {product_id} не найден.")

    return product


async def create_product(db: AsyncSession, new_product_data: ProductCreate, current_user_id: uuid.UUID):
    category = await db.get(models.Category, new_product_data.category_id)

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Категория с ID {new_product_data.category_id} не найдена.")

    new_product = models.Product(**new_product_data.dict(), creator_id=current_user_id)

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


async def delete_product(db: AsyncSession, product_id: uuid.UUID):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalars().one()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Продукт с ID {product_id} не найден.")

    await db.delete(product)
    await db.commit()

    return True


async def update_product(db: AsyncSession, product_id: uuid.UUID, current_user_id: uuid.UUID,
                         update_product_data: ProductUpdate):
    values = update_product_data.dict(exclude_unset=True)

    if not values:
        return

    product = await db.get(models.Product, product_id)

    if not product or not product.creator_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Продукт с ID {product_id} не найден.")

    category_id = values.get('category_id')

    if category_id:
        category = await db.get(models.Category, category_id)

        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Категория с ID {category_id} не найдена.")

    for key, value in values.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)

    return product
