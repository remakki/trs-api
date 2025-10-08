from faststream.rabbit.fastapi import RabbitRouter

from src import log
from src.config import settings
from src.digests.schemas import Digest

rabbit_router = RabbitRouter(settings.RABBITMQ_URL, include_in_schema=False)


async def publish_new_digest(digest: Digest) -> None:
    log.info("Publishing new digest notification...", storyline=digest.to_dict())
    await rabbit_router.publisher().publish(digest, "digest_notification")
