# Base database setup
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from todo_tracker.config import MainDBSettings

database_setings = MainDBSettings()

SQLALCHEMY_DATABASE_URL = (
    #    "postgresql+asyncpg://"
    #   f"{database_setings.DB_USERNAME}:{database_setings.DB_PASSWORD}"
    #   f"@{database_setings.DB_ADDRESS}/{database_setings.DB_NAME}"
    "postgresql+asyncpg://todo_user:local_dev@db:5432/todo_tracker"
)

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)


class Base(DeclarativeBase, AsyncAttrs):
    pass
