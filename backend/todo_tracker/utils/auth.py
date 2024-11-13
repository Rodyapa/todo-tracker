from sqlalchemy.ext.asyncio import AsyncSession

from todo_tracker.db.crud.user_crud import get_user_by_username
from todo_tracker.utils.password import verify_password


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(session=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
