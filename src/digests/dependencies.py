from src.database.config import sqlalchemy_config

from .services import DigestService

async def get_digest_service() -> DigestService:
    async with DigestService.new(config=sqlalchemy_config) as service:
        return service
