from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, String,JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.attempt import Attempt


class AttemptError(Base):
    __tablename__ = "attempt_errors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    attempt_id: Mapped[int] = mapped_column(ForeignKey("attempts.id"), nullable=False)
    error_type: Mapped[str] = mapped_column(String(20), nullable=False)
    severity: Mapped[Optional[str]] = mapped_column(String(20))
    details: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    attempt: Mapped["Attempt"] = relationship(back_populates="errors")