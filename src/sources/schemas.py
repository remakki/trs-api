from src.schemas import BaseSchema


class Source(BaseSchema):
    id: int
    title: str
    archive_url: str
    archive_token: str
