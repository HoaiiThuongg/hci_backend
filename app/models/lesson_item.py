from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON,Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.lesson import Lesson
    from app.models.attempt import Attempt
    from app.models.collector_sample import CollectorSample


class LessonItem(Base):
    __tablename__ = "lesson_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
    sign_label: Mapped[str] = mapped_column(String(100), nullable=False)
    item_type: Mapped[str] = mapped_column(String(10), nullable=False)  # static | dynamic
    difficulty: Mapped[Optional[int]] = mapped_column(Integer)  # 1..3
    description: Mapped[Optional[str]] = mapped_column(Text)
    reference_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    media: Mapped[dict] = mapped_column(JSON, nullable=False, server_default='{}')
    steps: Mapped[list] = mapped_column(JSON, nullable=False, server_default='[]')
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    lesson: Mapped["Lesson"] = relationship(back_populates="lesson_items")
    attempts: Mapped[List["Attempt"]] = relationship(back_populates="lesson_item", cascade="all, delete-orphan")
    collector_samples: Mapped[List["CollectorSample"]] = relationship(back_populates="lesson_item", cascade="all, delete-orphan")