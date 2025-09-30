from typing import Annotated, AsyncGenerator

from faststream import Depends as DependsFS

from src.database.config import sqlalchemy_config

from .services import TagService


async def provide_tag_service() -> AsyncGenerator[TagService, None]:
    async with TagService.new(config=sqlalchemy_config) as service:
        yield service


TagServiceDepFS = Annotated[TagService, DependsFS(provide_tag_service)]
