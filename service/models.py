"""SQLAlchemy ORM models."""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class URL(Base):
    """A shortened URL: its short code, target, and click stats."""

    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    short_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    long_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    click_count: Mapped[int] = mapped_column(Integer, default=0)
