from sqlalchemy.ext.asyncio import AsyncSession
from todo_tracker.db.models.task import Task
from todo_tracker.schemas import task_schemas
from datetime import datetime
from sqlalchemy import select, update
from typing import Optional
from fastapi import HTTPException
from typing import List


async def create_task(
        task_data: task_schemas.TaskCreate,
        session: AsyncSession,
        creator_id: int) -> Task:
    server_time = datetime.now(tz=None)
    task_db = Task(title=task_data.title,
                   description=task_data.description,
                   status=task_data.status,
                   created_at=server_time,
                   creator_id=creator_id)
    session.add(task_db)  # Add the task to the session
    await session.flush()  # Flush changes to the database
    await session.refresh(task_db, )  # Refresh to get the ID and state of the project
    return task_db


async def update_task(
        task_data: task_schemas.TaskUpdate,
        session: AsyncSession,
        task_id: int
) -> Optional[Task]:
    # Prepare the update statement
    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(**task_data.model_dump(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    # Execute the update statement
    await session.execute(stmt)
    await session.commit()  # Commit the transaction

    # Retrieve the updated task
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().first()
    return task


async def delete_task(
        task_id: int,
        session: AsyncSession) -> None | HTTPException:
    # Find if there is existing task
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(task)
    await session.commit()
    return None


async def get_task(
        task_id: int,
        session: AsyncSession
) -> Task:
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def get_tasks(
        session: AsyncSession
) -> List[Task]:
    stmt = select(Task)
    result = await session.execute(stmt)
    tasks = result.scalars()
    return tasks
