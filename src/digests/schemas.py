from datetime import datetime

from src.digests.models import DigestType
from src.schemas import BaseSchema


class DigestCreate(BaseSchema):
    type: DigestType
    start_time: datetime
    end_time: datetime
    source_id: int
    language: str
    to_chat_id: str


class DigestTag(BaseSchema):
    title: str
    quantity: int


class Digest(BaseSchema):
    id: int
    title: str
    summary: str
    type: DigestType
    start_time: datetime
    end_time: datetime
    created_at: datetime | None = None
    to_chat_id: str

    tags: list[DigestTag]
