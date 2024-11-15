from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from todo_tracker.db.models.user import User
from todo_tracker.schemas import user_schemas
from todo_tracker.utils.password import get_password_hash


async def create_user(
        user: user_schemas.UserCreate, session: AsyncSession) -> User:
    """
    Creates a new user in the database with a hashed password.

    Args:
        user (user_schemas.UserCreate): User data for creating a new user.
        session (AsyncSession): Database session.

    Returns:
        User: The created user with hashed password stored in the database.
    """
    hashed_pw = get_password_hash(user.password)

    db_user = User(username=user.username, password_hash=hashed_pw)

    async with session.begin():
        session.add(db_user)
        await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_username(
        username: str, session: AsyncSession) -> User | None:
    """
    Retrieves a user from the database by username.

    Args:
        username (str): The username of the user to retrieve.
        session (AsyncSession): Database session.

    Returns:
        User | None: The user with the specified username,
        or None if not found.
    """
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user
