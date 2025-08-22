from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings

engine = create_async_engine(settings.DB_URL_ASYNC)
async_session = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Генератор асинхронных сессий для FastAPI."""
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception as _:
        await session.rollback()
        raise
    finally:
        await session.close()
