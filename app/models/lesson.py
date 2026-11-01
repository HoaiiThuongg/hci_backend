from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.version import Version
    from app.models.lesson_item import LessonItem
    from app.models.user_lesson_progress import UserLessonProgress
    from app.models.attempt import Attempt


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    version_id: Mapped[int] = mapped_column(ForeignKey("versions.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    version: Mapped["Version"] = relationship(back_populates="lessons")
    lesson_items: Mapped[List["LessonItem"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")
    progresses: Mapped[List["UserLessonProgress"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")
    attempts: Mapped[List["Attempt"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")