from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from todo_list_api.settings import Settings

engine = create_async_engine(
    Settings().DATABASE_URL,
    max_overflow=10,
    pool_size=5,
    pool_recycle=200,
)


async def get_session():  # pragma: no cover
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
