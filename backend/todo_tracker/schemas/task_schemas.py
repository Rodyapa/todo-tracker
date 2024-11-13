from pydantic import BaseModel
from typing import Optional, List
from .user_schemas import UserRead
from todo_tracker.db.models.task import Task, TaskStatus
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    status: Optional[TaskStatus] = TaskStatus.PLANNED


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.PLANNED


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    creator_id: int
    status: TaskStatus
