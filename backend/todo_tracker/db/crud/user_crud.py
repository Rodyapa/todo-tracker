from sqlalchemy.ext.asyncio import AsyncSession
from todo_tracker.db.models.user import User
from todo_tracker.schemas import user_schemas
from todo_tracker.utils.password import get_password_hash


async def create_user(user: user_schemas.UserCreate,
                      session: AsyncSession) -> User:
    hashed_pw = get_password_hash(user.password)

    db_user = User(username=user.username,
                   password_hash=hashed_pw)

    async with session.begin():
        session.add(db_user)
        await session.commit()
    await session.refresh(db_user)
    return db_user