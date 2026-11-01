from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON,BigInteger, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.attempt import Attempt


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id"), unique=True, nullable=False)
    mode: Mapped[str] = mapped_column(String(10), nullable=False)
    level: Mapped[Optional[int]] = mapped_column(Integer)
    target_error_type: Mapped[Optional[str]] = mapped_column(String(20))
    message: Mapped[Optional[str]] = mapped_column(Text)
    suggested_action: Mapped[Optional[str]] = mapped_column(Text)
    media: Mapped[dict] = mapped_column(JSON, nullable=False, server_default='{}')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    attempt: Mapped["Attempt"] = relationship(back_populates="feedback")