from typing import Annotated, AsyncGenerator

from fastapi import Depends

from src.database.config import sqlalchemy_config

from .services import StorylineService


async def provide_storyline_service() -> AsyncGenerator[StorylineService, None]:
    async with StorylineService.new(config=sqlalchemy_config) as service:
        yield service


async def get_storyline_service() -> StorylineService:
    async with StorylineService.new(config=sqlalchemy_config) as service:
        return service


StorylineServiceDep = Annotated[StorylineService, Depends(provide_storyline_service)]
