from typing import Annotated

from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db import models
from src.db.db import get_db
from src.oauth import generate_token
from src.schemas.auth import Token, TokenData
from src.utils import verify_password

router = APIRouter(tags=['Аутентификация и регистрация'])


@router.post('/login', response_model=Token)
async def login(email: Annotated[str, Form()], password: Annotated[str, Form()], db: AsyncSession = Depends(get_db)):
    if not email and password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Форма должна быть заполнена')

    result = await db.execute(select(models.User).where(models.User.email == email))
    user = result.scalars().first()  # Use scalars to get the user object

    if not user or not await verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверно введены почта или пароль')

    token = await generate_token(TokenData(email=email, user_id=str(user.id)))
    return {'access_token': token, 'type': 'bearer'}
