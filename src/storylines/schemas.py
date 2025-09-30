from datetime import datetime

from src.schemas import BaseSchema
from src.sources.schemas import Source


class StorylineMessage(BaseSchema):
    start_time: datetime
    end_time: datetime
    title: str
    summary: str
    summary_ru: str
    temperature: str

    source_id: int

    tags: list[str]


class Storyline(BaseSchema):
    id: int
    title: str
    summary: str
    summary_ru: str
    temperature: str
    start_time: datetime
    end_time: datetime

    tags: list[str]

    source: Source
