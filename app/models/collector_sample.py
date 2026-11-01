from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, BigInteger, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.lesson_item import LessonItem
    from app.models.user import User


class CollectorSample(Base):
    __tablename__ = "collector_samples"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    lesson_item_id: Mapped[int] = mapped_column(ForeignKey("lesson_items.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    landmarks: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Đổi tên biến Python thành sample_metadata, nhưng ánh xạ cột DB là "metadata"
    sample_metadata: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, server_default='{}')
    
    validation_status: Mapped[str] = mapped_column(String(20), nullable=False, default='pending')
    validation_message: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    lesson_item: Mapped["LessonItem"] = relationship(back_populates="collector_samples")
    user: Mapped[Optional["User"]] = relationship(back_populates="collector_samples")