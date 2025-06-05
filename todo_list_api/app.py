from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from todo_list_api.schemas import (
    MessageClass,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='ToDo List API')
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageClass)
def read_root():
    return {'message': 'Hello World!'}


@app.get(
    '/api/v1/hello-world',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
def read_hello_world():
    return '<html><body><h1>Hello World!</h1></body></html>'


@app.post(
    '/api/v1/users',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
def create_user(user: UserSchema):
    user_with_id = UserPublic(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get(
    '/api/v1/users',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users():
    return {'users': database}


@app.put(
    '/api/v1/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            detail='User not found.', status_code=HTTPStatus.NOT_FOUND
        )

    user_with_id = UserPublic(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/api/v1/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def remove_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            detail='User not found.', status_code=HTTPStatus.NOT_FOUND
        )

    return database.pop(user_id - 1)


@app.get(
    '/api/v1/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def get_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            detail='User not found.', status_code=HTTPStatus.NOT_FOUND
        )

    return database[user_id - 1]
