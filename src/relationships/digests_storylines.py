from advanced_alchemy.base import orm_registry
from sqlalchemy import Column, ForeignKey, Table

digest_storyline_table = Table(
    "digests_storylines",
    orm_registry.metadata,
    Column("digest_id", ForeignKey("digests.id", ondelete="CASCADE"), primary_key=True),
    Column("storyline_id", ForeignKey("storylines.id", ondelete="CASCADE"), primary_key=True),
)
