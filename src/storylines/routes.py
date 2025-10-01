from faststream.rabbit import RabbitRouter, RabbitQueue

from src import log
from src.storylines.dependencies import StorylineServiceDepFS
from src.storylines.schemas import StorylineMessage
from src.tags.dependencies import TagServiceDepFS

rabbit_router = RabbitRouter()

@rabbit_router.subscriber(RabbitQueue(name='new_storyline', durable=True))
async def storyline_handler(
    message: StorylineMessage,
    storyline_service: StorylineServiceDepFS,
    tag_service: TagServiceDepFS
) -> None:
    log.info(f"Received new storyline message: {message.model_dump()}")
    await storyline_service.create_storyline(message, tag_service)
