from advanced_alchemy.base import orm_registry
from sqlalchemy import Column, ForeignKey, Table

storyline_tag_table = Table(
    "storylines_tags",
    orm_registry.metadata,
    Column("storyline_id", ForeignKey("storylines.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
