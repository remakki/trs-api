from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.relationships import digest_storyline_table, storyline_tag_table
from src.sources.models import SourceModel

if TYPE_CHECKING:
    from src.digests.models import DigestModel
    from src.tags.models import TagModel


class StorylineModel(BigIntAuditBase):
    """Storyline model."""

    __tablename__ = "storylines"

    start_time: Mapped[datetime]  # utc
    end_time: Mapped[datetime]  # utc
    title: Mapped[str]
    summary: Mapped[str]
    summary_ru: Mapped[str | None]
    temperature: Mapped[str]

    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False)

    source: Mapped["SourceModel"] = relationship(lazy="joined")

    tags: Mapped[list["TagModel"]] = relationship(
        secondary=storyline_tag_table,
        back_populates="storylines",
        lazy="selectin",
    )

    digests: Mapped[list["DigestModel"]] = relationship(
        secondary=digest_storyline_table,
        back_populates="storylines",
        lazy="selectin",
    )
