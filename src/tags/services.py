from typing import Iterable

from advanced_alchemy.extensions.fastapi import service

from .models import TagModel
from .repositories import TagRepository


class TagService(service.SQLAlchemyAsyncRepositoryService[TagModel, TagRepository]):
    """Tag Service"""

    repository_type = TagRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    @staticmethod
    def _normalize_tag_names(names: Iterable[str]) -> list[str]:
        return [n.strip().lower() for n in names if n and n.strip()]

    async def create_tags(self, tags: list[str]) -> list[TagModel]:
        tag_names = self._normalize_tag_names(tags or [])

        existing_tags = await self.list(TagModel.name.in_(tag_names))
        existing_by_name = [t.name for t in existing_tags]

        new_tags = [
            await self.create(TagModel(name=name))
            for name in tag_names
            if name not in existing_by_name
        ]

        new_tags.extend(existing_tags)

        return new_tags
