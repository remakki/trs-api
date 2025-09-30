from typing import Annotated, AsyncGenerator

from faststream import Depends as DependsFS

from src.database.config import sqlalchemy_config

from .services import StorylineService


async def provide_storyline_service() -> AsyncGenerator[StorylineService, None]:
    async with StorylineService.new(config=sqlalchemy_config) as service:
        yield service

async def get_storyline_service() -> StorylineService:
    async with StorylineService.new(config=sqlalchemy_config) as service:
        return service


StorylineServiceDepFS = Annotated[StorylineService, DependsFS(provide_storyline_service)]
