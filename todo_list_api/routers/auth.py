from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_list_api.database import get_session
from todo_list_api.models import User
from todo_list_api.schemas import Token
from todo_list_api.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user_db = session.scalar(
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
