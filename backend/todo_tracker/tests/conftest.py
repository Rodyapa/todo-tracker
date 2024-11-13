import uuid

import httpx
import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.pool import NullPool

from todo_tracker.db.base import Base
from todo_tracker.db.crud import user_crud
from todo_tracker.dependencies.db_dependencies import get_session
from todo_tracker.dependencies.env_dependencies import get_testing_settings
from todo_tracker.main import app
from todo_tracker.schemas import user_schemas
from todo_tracker.utils.jwt import create_access_token

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


@pytest_asyncio.fixture(scope="function", autouse=True)
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


# User related fixtures
@pytest_asyncio.fixture
def test_password():
    return 'strong-test-password'


@pytest_asyncio.fixture
def random_user_info(test_password):
    """return randomuser info"""
    user_data = {
        "username": str(uuid.uuid4()),
        "password": test_password
    }
    return user_data


@pytest_asyncio.fixture(scope='function')
async def create_new_user(test_password: str):
    '''Yield new user instances'''
    async def make_user(**kwargs):
        if 'password' not in kwargs:
            kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        user_data = user_schemas.UserCreate(**kwargs)
        async for session in get_test_session():
            user = await user_crud.create_user(session=session, user=user_data)
        return user
    yield make_user


# JWT Fixtures

@pytest_asyncio.fixture
async def get_authorization_header():
    async def make_header(**kwargs):
        access_token = await create_access_token(
            data={"sub": kwargs['user'].username}
        )
        headers = {"Authorization": f"Bearer {access_token}", }
        return headers
    yield make_header
