from advanced_alchemy.extensions.fastapi import service

from .models import SourceModel
from .repositories import SourceRepository


class SourceService(service.SQLAlchemyAsyncRepositoryService[SourceModel, SourceRepository]):
    """Source Service"""

    repository_type = SourceRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)
