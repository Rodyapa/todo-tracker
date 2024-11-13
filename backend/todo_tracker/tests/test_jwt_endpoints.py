import os
from time import sleep

import pytest
import pytest_asyncio

from todo_tracker.utils.jwt import create_access_token, create_refresh_token

pytestmark = pytest.mark.asyncio(loop_scope="function")


# ENV Variable fixtures
@pytest_asyncio.fixture(scope='function')
async def set_access_token_lifetime_to_zero():
    async def set_token_lifetime():
        os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = 0.1
    yield set_token_lifetime


async def test_user_can_get_access_token(async_client,
                                         create_new_user):
    # Arrange
    user_password = 'password'
    user = await create_new_user(password=user_password)
    url = '/auth/login'
    auth_data = {'username': user.username,
                 'password': user_password}
    # Act
    response = await async_client.post(url, data=auth_data)

    # Assert
    assert response.status_code == 200
    assert 'access_token' in response.json(), (
        'Response must contains access token'
    )
    assert 'refresh_token' in response.json(), (
        'Response must contains refresh token'
    )


async def test_user_can_refresh_token(async_client,
                                      create_new_user,
                                      set_access_token_lifetime_to_zero):
    # Arrange
    user_password = 'password'
    user = await create_new_user(password=user_password)
    access_token = await create_access_token(
        data={'sub': user.username}
    )
    refresh_token = await create_refresh_token(
        data={'sub': user.username}
    )
    url = '/auth/refresh'
    # Act
    sleep(1)  # TODO find solution without sleep function
    response = await async_client.post(url,
                                       json={'refresh_token': refresh_token, })

    # Assert
    assert response.status_code == 200
    assert 'access_token' in response.json(), (
        'Response must contains access token'
    )
    new_access_token = response.json()['access_token']
    assert access_token != new_access_token, (
        'Response must contains updated access token'
    )
    assert 'refresh_token' in response.json(), (
        'Response must contains refresh token'
    )
    new_refresh_token = response.json()['refresh_token']
    assert refresh_token != new_refresh_token, (
        'Response must contains updated refresh token'
    )
