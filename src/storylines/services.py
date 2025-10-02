from advanced_alchemy.extensions.fastapi import service

from ..tags.services import TagService
from .models import StorylineModel
from .repositories import StorylineRepository
from .schemas import StorylineMessage


class StorylineService(
    service.SQLAlchemyAsyncRepositoryService[StorylineModel, StorylineRepository]
):
    """Storyline Service"""

    repository_type = StorylineRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)
        self._tag_service = TagService(session=session)

    async def create_storyline(self, message: StorylineMessage) -> StorylineModel:
        tags = await self._tag_service.create_tags(message.tags)
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

        return new_storyline
