from faststream.rabbit import RabbitRouter, RabbitQueue

from src.sources.schemas import Source
from src.storylines.models import StorylineModel
from src.storylines.schemas import Storyline

rabbit_router = RabbitRouter()

@rabbit_router.publisher(RabbitQueue(name='storyline_notification', durable=True))
async def publish_new_storyline(storyline: StorylineModel) -> Storyline:
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
        temperature=storyline.temperature
    )
