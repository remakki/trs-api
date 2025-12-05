from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter

from src import log
from src.config import settings
from src.sources.schemas import Source
from src.storylines.dependencies import StorylineServiceDep
from src.storylines.schemas import StorylineMessage, Storyline

rabbit_router = RabbitRouter(settings.RABBITMQ_URL, include_in_schema=False)


@rabbit_router.subscriber(RabbitQueue(name="new_storyline", durable=True))
@rabbit_router.publisher(RabbitQueue(name="storyline_notification", durable=True))
async def storyline_handler(
    message: StorylineMessage,
    storyline_service: StorylineServiceDep,
) -> Storyline:
    log.info("Received new storyline message", message=message.model_dump())
    try:
        storyline = await storyline_service.create_storyline(message)
    except Exception as e:
        log.error(f"Error creating storyline", error=str(e))
        raise
    log.info("Publishing new storyline notification...", storyline=storyline.to_dict())
    return Storyline(
        id=storyline.id,
        title=storyline.title,
        tags=[tag.name for tag in storyline.tags],
        source=Source(
            id=storyline.source.id,
            title=storyline.source.title,
            archive_url=storyline.source.archive_url,
            archive_token=storyline.source.archive_token,
        ),
        summary=storyline.summary,
        summary_ru=storyline.summary_ru,
        start_time=storyline.start_time,
        end_time=storyline.end_time,
        temperature=storyline.temperature,
        to_chat_id=storyline.source.chat_id,
    )
