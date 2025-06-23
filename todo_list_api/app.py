from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todo_list_api.database import get_session
from todo_list_api.models import User
from todo_list_api.schemas import (
    MessageClass,
    Token,
    UserList,
    UserPublic,
    UserSchema,
)
from todo_list_api.security import (
    create_access_token,
    get_password_hash,
    verify_password,
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
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    if db_user := session.scalar(
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
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    '/api/v1/users',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
def read_users(
    session: Session = Depends(get_session),
    limit: int = 10,
    offset: int = 0,
):
    return {'users': session.scalars(select(User).limit(limit).offset(offset))}


@app.put(
    '/api/v1/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User doesnt exist!'
        )
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = get_password_hash(user.password)

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError as e:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists!',
        ) from e


@app.delete(
    '/api/v1/users/{user_id}',
    status_code=HTTPStatus.NO_CONTENT,
)
def remove_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User doesnt exist!'
        )

    session.delete(user_db)
    session.commit()


@app.get(
    '/api/v1/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def read_user(user_id: int, session: Session = Depends(get_session)):
    if user_db := session.scalar(select(User).where(User.id == user_id)):
        return user_db
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User doesnt exist!'
        )


@app.post('/api/v1/token/', response_model=Token)
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
