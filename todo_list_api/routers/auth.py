from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_list_api.database import get_session
from todo_list_api.models import User
from todo_list_api.schemas import Token
from todo_list_api.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])

Session = Annotated[AsyncSession, Depends(get_session)]
OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuthForm,
    session: Session,
):
    user_db = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Email doesnt exists!',
        )

    if not verify_password(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect password!',
        )

    access_token = create_access_token({'sub': user_db.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'Bearer'}
