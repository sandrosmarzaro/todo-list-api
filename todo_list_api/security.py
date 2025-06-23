from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import encode
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from todo_list_api.database import get_session

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='/api/v1/token')

SECRET_KEY = ''
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    claims = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    claims['exp'] = expire

    return encode(claims, SECRET_KEY, algorithm=ALGORITHM)
