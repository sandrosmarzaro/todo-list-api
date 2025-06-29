from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from todo_list_api.database import get_session
from todo_list_api.models.users import User
from todo_list_api.schemas.filters import FilterPage
from todo_list_api.schemas.users import (
    UserCreate,
    UserResponse,
    UserResponseList,
    UserUpdate,
)
from todo_list_api.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/api/v1/users', tags=['users'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
FilterUsers = Annotated[FilterPage, Query()]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserResponse,
)
async def create_user(user: UserCreate, session: Session):
    if db_user := await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    ):
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists!',
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists!',
                status_code=HTTPStatus.CONFLICT,
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=UserResponseList,
)
async def read_users(
    session: Session,
    current_user: CurrentUser,
    filters: FilterUsers,
):
    return {
        'users': await session.scalars(
            select(User).limit(filters.limit).offset(filters.offset)
        )
    }


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )
    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

        return current_user
    except IntegrityError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists!',
        ) from e


@router.delete(
    '/{user_id}',
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
)
async def remove_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    await session.delete(current_user)
    await session.commit()


@router.get(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserResponse,
)
async def read_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )
    return current_user
