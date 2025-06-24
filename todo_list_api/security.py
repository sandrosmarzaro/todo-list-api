from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from todo_list_api.database import get_session
from todo_list_api.models import User
from todo_list_api.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')
settings = Settings()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    claims = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    claims['exp'] = expire

    return encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception
    except DecodeError as e:
        raise credentials_exception from e

    if user_db := session.scalar(
        select(User).where(User.email == subject_email)
    ):
        return user_db
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User doesnt exists',
        )
