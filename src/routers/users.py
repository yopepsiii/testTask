import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import models
from src.db.db import get_db
from src.oauth import get_current_user
from src.schemas.auth import TokenData
from src.schemas.user import UserCreate, UserUpdate, UserFullInfo
from src.cruds.users import create_user, update_user, delete_user

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/", response_model=UserFullInfo, status_code=status.HTTP_201_CREATED)
async def register_new_user(new_user_json: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(new_user_json, db)


@router.patch("/me", response_model=UserFullInfo)
async def update_user_data(updated_data_json: UserUpdate, current_user_data: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await update_user(uuid.UUID(current_user_data.user_id), updated_data_json, db)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(current_user_data: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await delete_user(uuid.UUID(current_user_data.user_id), db)
