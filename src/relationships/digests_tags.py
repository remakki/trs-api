# from sqlalchemy import Table, Column, ForeignKey
# from advanced_alchemy.base import orm_registry
#
# digest_tag_table = Table(
#     "digests_tags",
#     orm_registry.metadata,
#     Column("digest_id", ForeignKey("digests.id", ondelete="CASCADE"), primary_key=True),
#     Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
# )
