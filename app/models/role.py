from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Role(BaseModel):
    """Database model representing user roles and permissions."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    # description: Mapped[Optional[str]] = mapped_column(
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships
    users: Mapped[list[User]] = relationship(
        back_populates="role",
    )
