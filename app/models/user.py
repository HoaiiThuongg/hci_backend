from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user_lesson_progress import UserLessonProgress
    from app.models.attempt import Attempt
    from app.models.collector_sample import CollectorSample
    from app.models.app_settings import AppSettings


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    display_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    progresses: Mapped[List["UserLessonProgress"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    attempts: Mapped[List["Attempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    collector_samples: Mapped[List["CollectorSample"]] = relationship(back_populates="user")
    updated_settings: Mapped[List["AppSettings"]] = relationship(back_populates="updater")