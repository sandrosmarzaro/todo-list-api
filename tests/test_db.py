import contextlib
from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_list_api.database import get_session
from todo_list_api.models import User


@pytest.mark.asyncio
async def test_should_create_user_in_db(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='test_name', email='test@email.com', password='test1234'
        )
        session.add(new_user)
        await session.commit()

        user = await session.scalar(select(User).where(User.id == 1))

        assert user.username == 'test_name'
        assert user.email == 'test@email.com'
        assert user.password == 'test1234'
        assert asdict(user) == {
            'id': 1,
            'username': 'test_name',
            'email': 'test@email.com',
            'password': 'test1234',
            'created_at': time,
            'updated_at': time,
        }


@pytest.mark.asyncio
async def test_get_session_yields_async_session():
    session = get_session()
    async_session = await anext(session)

    try:
        assert isinstance(async_session, AsyncSession)

    finally:
        with contextlib.suppress(StopAsyncIteration):
            await anext(session)
