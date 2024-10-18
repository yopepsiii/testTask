from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.cruds.categories import get_categories, create_category, delete_category
from src.db.db import get_db
from src.oauth import get_current_user
from src.schemas.auth import TokenData
from src.schemas.category import CategoryOut, CategoryCreate

router = APIRouter(prefix='/categories', tags=['Категории продуктов'])


@router.get('/', response_model=list[CategoryOut])
async def get_categories_endpoint(db: AsyncSession = Depends(get_db),
                                  current_user_data: TokenData = Depends(get_current_user)):
    return await get_categories(db)


@router.post('/', response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(category_data: CategoryCreate, db: AsyncSession = Depends(get_db), current_user_data: TokenData = Depends(get_current_user)):
    return await create_category(db, category_data)


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_db), current_user_data: TokenData = Depends(get_current_user)):
    return await delete_category(db, category_id)
