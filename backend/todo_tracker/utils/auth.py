from sqlalchemy.ext.asyncio import AsyncSession

from todo_tracker.db.crud.user_crud import get_user_by_username
from todo_tracker.utils.password import verify_password


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    Authenticates a user by verifying their username and password.

    Args:
        db (AsyncSession): Database session used to query the user.
        username (str): The username provided for authentication.
        password (str): The plaintext password provided for authentication.

    Returns:
        User | bool: Returns the authenticated `User` object if successful,
                     or `False` if authentication fails.

    """
    user = await get_user_by_username(session=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
