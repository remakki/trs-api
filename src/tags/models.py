from typing import TYPE_CHECKING

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.relationships.storylines_tags import storyline_tag_table

if TYPE_CHECKING:
    from src.storylines.models import StorylineModel


class TagModel(BigIntAuditBase):
    """Tag model."""

    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(127), unique=True)

    storylines: Mapped[list["StorylineModel"]] = relationship(
        secondary=storyline_tag_table,
        back_populates="tags",
        lazy="selectin",
        viewonly=True,
    )
