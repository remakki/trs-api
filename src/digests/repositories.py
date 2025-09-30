from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select, func

from .models import DigestModel
from .schemas import DigestTag
from ..relationships import digest_storyline_table, storyline_tag_table
from ..storylines.models import StorylineModel
from ..tags.models import TagModel


class DigestRepository(SQLAlchemyAsyncRepository[DigestModel]):
    """Digest repository"""

    model_type = DigestModel

    async def get_tags(self, digest_id: int) -> list[DigestTag]:
        stmt = (
            select(
                TagModel.id.label("tag_id"),
                TagModel.name.label("tag_name"),
                func.count().label("tag_count"),
            )
            .join(digest_storyline_table, DigestModel.id == digest_storyline_table.c.digest_id)
            .join(StorylineModel, StorylineModel.id == digest_storyline_table.c.storyline_id)
            .join(storyline_tag_table, StorylineModel.id == storyline_tag_table.c.storyline_id)
            .join(TagModel, TagModel.id == storyline_tag_table.c.tag_id)
            .where(DigestModel.id == digest_id)
            .group_by(TagModel.id, TagModel.name)
            .order_by(func.count().desc())
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        return [
            DigestTag(title=row.tag_name, quantity=row.tag_count) for row in rows
        ]
