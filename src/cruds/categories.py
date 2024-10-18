from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import models
from src.schemas.category import CategoryCreate


async def get_categories(db: AsyncSession):
    result = await db.execute(select(models.Category))
    categories = result.scalars().all()

    return categories


async def create_category(db: AsyncSession, new_category_data: CategoryCreate):
    new_category = models.Category(**new_category_data.dict())

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category


async def delete_category(db: AsyncSession, category_id: int):
    category = await db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Категория с ID {category_id} не найдена.")

    await db.delete(category)
    await db.commit()

    return True
