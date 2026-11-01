from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.lesson import Lesson


class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    completed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    best_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    last_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="progresses")
    lesson: Mapped["Lesson"] = relationship(back_populates="progresses")