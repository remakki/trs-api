from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.config import settings
from src.storylines.routes import rabbit_router as storyline_rabbit_router
from src.storylines.publisher import rabbit_router as storyline_publisher_rabbit_router
from src.digests.publisher import rabbit_router as digest_rabbit_router

broker = RabbitBroker(settings.RABBITMQ_URL)

faststream = FastStream(
    broker,
    title="TRS API Service",
    version="0.0.1",
)

broker.include_router(storyline_rabbit_router)
broker.include_router(storyline_publisher_rabbit_router)
broker.include_router(digest_rabbit_router)
