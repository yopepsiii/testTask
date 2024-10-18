import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import utils
from src.db import models
from src.schemas.user import UserCreate, UserUpdate
from src.utils import hash_password


async def create_user(user_data: UserCreate, db: AsyncSession):
    plain_password = user_data.password
    user_data.password = await hash_password(plain_password)

    new_user = models.User(**user_data.dict())

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def update_user(current_user_id: uuid.UUID, updated_user_data: UserUpdate, db: AsyncSession):
    values = updated_user_data.dict(exclude_unset=True)

    if not values:
        return

    if values.get('password'):
        values['password'] = await utils.hash_password(updated_user_data.password)

    current_user = await db.get(models.User, current_user_id)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ваш аккаунт не был найден.")

    for key, value in values.items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user


async def delete_user(current_user_id: uuid.UUID, db: AsyncSession):
    current_user = await db.get(models.User, current_user_id)

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ваш аккаунт не был найден.")

    await db.delete(current_user)
    await db.commit()

    return True
