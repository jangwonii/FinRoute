from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.session import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    advisor_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.user_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(40), nullable=True)
    occupation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    household_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    advisor = relationship("User", back_populates="customers")
