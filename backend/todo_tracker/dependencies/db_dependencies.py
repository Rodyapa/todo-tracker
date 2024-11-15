from todo_tracker.db.base import async_session_factory


async def get_session():
    """
    Provides a database session for use in asynchronous operations.

    This function yields a session using the `async_session_factory`,
    ensuring that the session is properly opened and closed
    around each database operation.

    Yields:
        AsyncSession: A database session for executing queries
        within an async context.
    """
    async with async_session_factory() as session:
        yield session
