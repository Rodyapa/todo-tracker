import enum
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy import func as sql_function_generator
from sqlalchemy.orm import Mapped, mapped_column

from todo_tracker.db.base import Base


class TaskStatus(str, enum.Enum):
    PLANNED = "запланирована"
    IN_PROGRESS = "в процессе"
    COMPLETED = "завершена"


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PLANNED)

    # Additional fields
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=sql_function_generator.now())
    creator_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL"),
        nullable=True)
