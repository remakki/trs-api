from datetime import datetime
from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.relationships import storyline_tag_table

if TYPE_CHECKING:
    from src.tags.models import TagModel
    from src.sources.models import SourceModel


class StorylineModel(BigIntAuditBase):
    """Storyline model."""

    __tablename__ = "storylines"

    start_time: Mapped[datetime]  # utc
    end_time: Mapped[datetime]  # utc
    title: Mapped[str]
    summary: Mapped[str]
    summary_ru: Mapped[str]
    temperature: Mapped[str]

    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=False)

    source: Mapped["SourceModel"] = relationship(lazy="joined")

    tags: Mapped[list["TagModel"]] = relationship(
        secondary=storyline_tag_table,
        back_populates="storylines",
        lazy="selectin",
    )
