import asyncio

import pytest
from sqlalchemy import func, select

from todo_tracker.db.models.user import User

from .conftest import async_test_session_factory

pytestmark = pytest.mark.asyncio(loop_scope="function")


async def test_create_user_endpoint_async(async_client):
    # ARRANGE
    user_datas = [{"username": "test_user1", "password": "strong_password"},
                  {"username": "test_user2", "password": "strong_password"},
                  {"username": "test_user3", "password": "strong_password"},
                  ]
    # Measure the time taken to send multiple requests simultaneously
    start_time = asyncio.get_event_loop().time()
    tasks = []
    for payload in user_datas:
        tasks.append(async_client.post("/auth/register", data=payload))

    # Run tasks concurrently
    responses = await asyncio.gather(*tasks)
    # Measure the total time taken
    total_time = asyncio.get_event_loop().time() - start_time

    # Assert that all responses are successful
    for response in responses:
        assert response.status_code == 201

    # Assert there are three instances of user in the Database
    async with async_test_session_factory() as session:
        db_user_counter = await (session.scalar(select(func.count())
                                                .select_from(User)))
        assert db_user_counter == 3, 'There must be 3 created users in the DB'
    # Check that the total time taken is shorter than if processed sequentially
    # Assuming each request takes about 1 second,
    # concurrent should be <3 seconds
    assert total_time < 3, "Requests did not complete concurrently as expected"
