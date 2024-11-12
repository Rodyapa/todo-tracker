from todo_tracker.db.base import async_session_factory


async def get_session():
    async with async_session_factory() as session:
        yield session
