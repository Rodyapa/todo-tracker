from fastapi import APIRouter
from todo_tracker.schemas import task_schemas
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from todo_tracker.dependencies.db_dependencies import get_session
from todo_tracker.db.crud import task_crud
from todo_tracker.db.models.task import Task, TaskStatus
from todo_tracker.dependencies.jwt_dependencies import get_current_user
from todo_tracker.db.models.user import User
from typing import List, Optional


router = APIRouter(
    prefix='/tasks',
    tags=['Tasks', ],
    responses={404: {"description": "Not found"}},
)


# POST REQUESTS
@router.post('', status_code=status.HTTP_201_CREATED,
             response_model=task_schemas.TaskRead)
async def create_task(
    task_data: task_schemas.TaskCreate,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    task_db: Task = await task_crud.create_task(
        task_data=task_data, session=session,
        creator_id=user.id
    )
    await session.commit()
    return task_db


# GET REQUESTS
@router.get('', status_code=status.HTTP_200_OK,
            response_model=List[task_schemas.TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    status: Optional[TaskStatus] = None
):
    tasks: List[Task] = await task_crud.get_tasks(
        session=session,
        status=status
    )
    return tasks


@router.get("/{task_id}", status_code=status.HTTP_200_OK,
            response_model=task_schemas.TaskRead)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)):
    task_db: Task = await task_crud.get_task(
        session=session, task_id=task_id
    )
    return task_db


# PUT REQUESTS
@router.put("/{task_id}", status_code=status.HTTP_200_OK,
                 response_model=task_schemas.TaskRead,
                 )
async def update_task(
    task_data: task_schemas.TaskUpdate,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    task_db: Task = await task_crud.update_task(
        task_data=task_data, session=session,
        task_id=task_id
    )
    await session.commit()
    return task_db


# DELETE REQUESTS
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    await task_crud.delete_task(session=session, task_id=task_id)
