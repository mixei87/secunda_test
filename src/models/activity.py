from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    SmallInteger,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.core.config import settings


class Activity(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activity.id", ondelete="RESTRICT"), nullable=True
    )
    depth: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    __table_args__ = (
        CheckConstraint(
            f"depth >= 1 AND depth <= {settings.ACTIVITY_MAX_DEPTH}", 
            name="depth_range"
        ),
        UniqueConstraint("parent_id", "name"),
    )

    parent = relationship("Activity", remote_side=[id], backref="children")
