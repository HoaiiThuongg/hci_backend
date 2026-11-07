from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.lesson import Lesson
    from app.models.lesson_item import LessonItem
    from app.models.attempt_error import AttemptError
    from app.models.feedback import Feedback


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer(), 'sqlite'), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    lesson_item_id: Mapped[int] = mapped_column(ForeignKey("lesson_items.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean)
    predicted_sign: Mapped[Optional[str]] = mapped_column(String(100))
    model_confidence: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 4))
    score: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)
    feedback_mode: Mapped[str] = mapped_column(String(10), nullable=False)
    feedback_level_shown: Mapped[Optional[int]] = mapped_column(Integer)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="attempts")
    lesson: Mapped["Lesson"] = relationship(back_populates="attempts")
    lesson_item: Mapped["LessonItem"] = relationship(back_populates="attempts")
    errors: Mapped[List["AttemptError"]] = relationship(back_populates="attempt", cascade="all, delete-orphan")
    feedback: Mapped[Optional["Feedback"]] = relationship(back_populates="attempt", uselist=False, cascade="all, delete-orphan")