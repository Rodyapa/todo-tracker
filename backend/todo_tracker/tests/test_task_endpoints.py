import pytest
import pytest_asyncio

from todo_tracker.tests.conftest import get_test_session

from todo_tracker.db.models.task import Task
from todo_tracker.db.models.user import User
import uuid
from typing import Tuple

pytestmark = pytest.mark.asyncio(loop_scope="function")


@pytest_asyncio.fixture(scope='function')
async def create_task(create_new_user) -> Tuple[User, Task]:
    async def make_task():
        user = await create_new_user()
        task_data = {
                'title': str(uuid.uuid4()),
                'description': str(uuid.uuid4()),
                'creator_id': user.id
            }
        task = Task(**task_data)
        async for session in get_test_session():
            session.add(task)
            await session.flush([task,])
            await session.refresh(task)
            await session.commit()
        return user, task
    yield make_task


@pytest_asyncio.fixture(scope='function')
async def get_random_task_data():
    def make_task_data(**kwargs):
        task_data = {
            'title': f'task {str(uuid.uuid4)[:8]}',
            'description': f'desription {str(uuid.uuid4)[:8]}'
        }
        return task_data
    yield make_task_data


class TestTaskAPI:
    '''Tests related to Tasks instances API actions'''
    async def test_user_can_create_task(self, async_client, create_new_user,
                                        get_authorization_header):
        user = await create_new_user()
        url = '/tasks'
        task_data = {
            'title': 'walk the dog',
            'description': 'very important',
        }
        headers = await get_authorization_header(user=user)
        response = await async_client.post(url=url,
                                           headers=headers,
                                           json=task_data)

        assert response.status_code == 201

    async def test_user_can_delete_task(self, async_client,
                                        get_authorization_header,
                                        create_task):
        task_creator, task = await create_task()
        task_id = task.id
        url = f'/tasks/{task_id}'

        headers = await get_authorization_header(user=task_creator)

        response = await async_client.delete(url=url, headers=headers)

        assert response.status_code == 204

    async def test_user_can_change_status_of_the_task(
            self, async_client, get_authorization_header, create_task):
        task_creator, task = await create_task()
        task_id = task.id
        url = f'/tasks/{task_id}'

        new_task_data = {
            'status': 'завершена',
        }

        headers = await get_authorization_header(user=task_creator)

        response = await async_client.put(url=url, json=new_task_data,
                                          headers=headers)

        assert response.status_code == 200
        assert response.json()['status'] == 'завершена', (
            'Task status should be changed after put request.')

    async def test_user_cannot_change_status_with_invalid_valaue(
            self, async_client, get_authorization_header, create_task):

        task_creator, task = await create_task()
        task_id = task.id
        url = f'/tasks/{task_id}'

        new_task_data = {
            'status': 'Um, mostly completed, but actually...',
        }

        headers = await get_authorization_header(user=task_creator)

        response = await async_client.put(url=url, json=new_task_data,
                                          headers=headers)

        assert response.status_code == 422

    async def test_user_can_get_task_information(
            self, async_client, create_task):

        task_creator, task = await create_task()
        task_id = task.id
        url = f'/tasks/{task_id}'

        response = await async_client.get(url=url)

        assert response.status_code == 200
        expected_fields = ['title', 'description', 'id',
                           'creator_id', 'created_at', 'status',]
        for field in expected_fields:
            assert field in response.json(), (
                f'Field {field} must be in the response data'
            )

    async def test_user_can_get_all_tasks(
        self, async_client, create_task
    ):
        tasks = [await create_task() for task in range(3)]

        url = '/tasks'
        response = await async_client.get(url)

        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list), (
            'Response must contains list of tasks')
        assert len(response_data) == 3, (
            'Response must contains list of tasks'
            'populated with 3 task instances'
        )
