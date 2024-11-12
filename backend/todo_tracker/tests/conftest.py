import httpx
import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.pool import NullPool

from todo_tracker.db.base import Base
from todo_tracker.dependencies.db_dependencies import get_session
from todo_tracker.dependencies.env_dependencies import get_testing_settings
from todo_tracker.main import app

database_data = get_testing_settings()

# Data for connection to test_database
SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{database_data.TEST_DB_USERNAME}:"
    f"{database_data.TEST_DB_PASSWORD}"
    f"@{database_data.TEST_DB_ADDRESS}/{database_data.TEST_DB_NAME}"
    )
# Instance of Async Engine connected to described database
async_engine = create_async_engine(
    SQLALCHEMY_TEST_DATABASE_URL, echo=False,
    poolclass=NullPool
)

async_test_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)


async def get_test_session() -> AsyncSession:
    async with async_test_session_factory() as session:
        yield session
        await session.close()

app.dependency_overrides[get_session] = get_test_session


# Initialize test database tables
async def init_models(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Drop tables after tests are completed
async def drop_models(async_engine: AsyncEngine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    print("Creating tables...")  # For debugging
    await init_models(async_engine)
    yield
    print("Dropping tables...")  # For debugging
    await drop_models(async_engine)
    print("Tables dropped")


@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient(
        base_url="http://test",
        transport=httpx.ASGITransport(app=app)
    ) as client:
        yield client
        await client.aclose()
