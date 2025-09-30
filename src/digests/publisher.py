from faststream.rabbit import RabbitRouter, RabbitQueue

from src.digests.models import DigestModel
from src.digests.schemas import Digest, DigestTag

rabbit_router = RabbitRouter()

@rabbit_router.publisher(RabbitQueue(name='digest_notification', durable=True))
async def publish_new_digest(digest: DigestModel, tags: list[DigestTag]) -> Digest:
    return Digest(
        id=digest.id,
        title=digest.title,
        tags=tags,
        summary=digest.summary,
        type=digest.type,
        start_time=digest.start_time,
        end_time=digest.end_time,
    )
