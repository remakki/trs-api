from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.enums import BaseEnum
from src.relationships import digest_storyline_table

if TYPE_CHECKING:
    # from src.tags.models import TagModel
    from src.storylines.models import StorylineModel


class DigestType(BaseEnum):
    DAILY = "daily"
    CUSTOM = "custom"


class DigestModel(BigIntAuditBase):
    """Digest model."""

    __tablename__ = "digests"

    title: Mapped[str]
    summary: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    type: Mapped[DigestType] = mapped_column(SQLEnum(DigestType, name="digest_type"))

    storylines: Mapped[list["StorylineModel"]] = relationship(
        secondary=digest_storyline_table,
        back_populates="digests",
        lazy="selectin",
    )

    # tags: Mapped[list["TagModel"]] = relationship(
    #     secondary=digest_tag_table,
    #     back_populates="digests",
    #     lazy="selectin",
    # )
