from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_list_api.database import get_session
from todo_list_api.models.todos import Todo
from todo_list_api.models.users import User
from todo_list_api.schemas.filters import FilterTodo
from todo_list_api.schemas.todos import (
    TodoCreate,
    TodoResponse,
    TodoResponseList,
    TodoUpdate,
)
from todo_list_api.security import get_current_user

router = APIRouter(prefix='/api/v1/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterTodo, Query()]


@router.post(
    '/',
    response_model=TodoResponse,
    status_code=HTTPStatus.CREATED,
)
async def create_todo(
    todo: TodoCreate,
    session: Session,
    current_user: CurrentUser,
):
    todo_db = Todo(
        user_id=current_user.id,
        title=todo.title,
        description=todo.description,
        state=todo.state,
    )

    session.add(todo_db)
    await session.commit()
    await session.refresh(todo_db)

    return todo_db


@router.get(
    '/',
    response_model=TodoResponseList,
    status_code=HTTPStatus.OK,
)
async def read_todos(
    session: Session, current_user: CurrentUser, filters: Filter
):
    query = select(Todo).where(Todo.user_id == current_user.id)

    filter_data = filters.model_dump(
        exclude_unset=True, exclude={'limit', 'offset'}
    )

    for field_name, field_value in filter_data.items():
        if hasattr(Todo, field_name):
            column = getattr(Todo, field_name)

            if field_name in {'title', 'description'}:
                query = query.filter(column.contains(field_value))
            else:
                query = query.filter(column == field_value)

    todos = await session.scalars(
        query.limit(filters.limit).offset(filters.offset)
    )

    return {'todos': todos.all()}


@router.delete(
    '/{todo_id}',
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_todo(
    todo_id: int, session: Session, current_user: CurrentUser
):
    todo = await session.scalar(
        select(Todo).where(todo_id == Todo.id, current_user.id == Todo.user_id)
    )
    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task dont exists'
        )

    await session.delete(todo)
    await session.commit()


@router.patch(
    '/{todo_id}', response_model=TodoResponse, status_code=HTTPStatus.OK
)
async def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: Session,
    current_user: CurrentUser,
):
    todo_db = await session.scalar(
        select(Todo).where(todo_id == Todo.id, current_user.id == Todo.user_id)
    )
    if not todo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task dont exists'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(todo_db, key, value)

    session.add(todo_db)
    await session.commit()
    await session.refresh(todo_db)

    return todo_db
