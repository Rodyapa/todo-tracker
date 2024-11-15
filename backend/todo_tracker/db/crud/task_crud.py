from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from todo_tracker.db.models.task import Task, TaskStatus
from todo_tracker.schemas import task_schemas


async def create_task(
        task_data: task_schemas.TaskCreate,
        session: AsyncSession,
        creator_id: int) -> Task:
    """
    Adds a new task record to the database.

    Args:
        task_data (task_schemas.TaskCreate): Data for creating a new task.
        session (AsyncSession): Database session.
        creator_id (int): ID of the user creating the task.

    Returns:
        Task: The mapped task object.
    """
    server_time = datetime.now(tz=None)
    task_db = Task(title=task_data.title,
                   description=task_data.description,
                   status=task_data.status,
                   created_at=server_time,
                   creator_id=creator_id)
    session.add(task_db)
    await session.flush()
    await session.refresh(task_db)
    return task_db


async def update_task(
        task_data: task_schemas.TaskUpdate,
        session: AsyncSession,
        task_id: int
) -> Optional[Task]:
    """
    Updates an existing task in the database.

    Args:
        task_data (task_schemas.TaskUpdate): Data for updating the task.
        session (AsyncSession): Database session.
        task_id (int): ID of the task to update.

    Returns:
        Optional[Task]: The updated task, or None if not found.
    """
    stmt = (
        update(Task)
        .where(Task.id == task_id)
        .values(**task_data.model_dump(exclude_unset=True))
        .execution_options(synchronize_session="fetch")
    )
    await session.execute(stmt)
    await session.commit()

    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().first()
    return task


async def delete_task(
        task_id: int,
        session: AsyncSession) -> None | HTTPException:
    """
    Deletes a task from the database.

    Args:
        task_id (int): ID of the task to delete.
        session (AsyncSession): Database session.

    Returns:
        None: If the deletion was successful.
        HTTPException: If the task was not found.
    """
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
    """
    Retrieves a task from the database by ID.

    Args:
        task_id (int): ID of the task to retrieve.
        session (AsyncSession): Database session.

    Returns:
        Task: The retrieved task.
    """
    stmt = select(Task).where(Task.id == task_id)
    result = await session.execute(stmt)
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def get_tasks(
        session: AsyncSession,
        status: Optional[TaskStatus] = None
) -> List[Task]:
    """
    Retrieves tasks from the database, optionally filtered by status.

    Args:
        session (AsyncSession): Database session.
        status (Optional[TaskStatus]): Optional status to filter tasks.

    Returns:
        List[Task]: A list of tasks, optionally filtered by status.
    """
    stmt = select(Task)
    if status:
        stmt = stmt.where(Task.status == status.value)
    result = await session.execute(stmt)
    tasks = result.scalars()
    return tasks
