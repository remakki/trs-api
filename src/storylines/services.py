from advanced_alchemy.extensions.fastapi import service

from .models import StorylineModel
from .publisher import publish_new_storyline
from .repositories import StorylineRepository
from .schemas import StorylineMessage
from ..tags.services import TagService


class StorylineService(service.SQLAlchemyAsyncRepositoryService[StorylineModel, StorylineRepository]):
    """Storyline Service"""

    repository_type = StorylineRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    async def create_storyline(self, message: StorylineMessage, tag_service: TagService) -> StorylineModel:
        tags = await tag_service.create_tags(message.tags)
        storyline = StorylineModel(
            start_time=message.start_time,
            end_time=message.end_time,
            title=message.title,
            summary=message.summary,
            summary_ru=message.summary_ru,
            temperature=message.temperature,
            source_id=message.source_id,
            tags=tags,
        )
        new_storyline = await self.create(storyline)

        await publish_new_storyline(new_storyline)

        return new_storyline
