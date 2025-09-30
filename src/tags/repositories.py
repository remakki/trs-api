from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import TagModel


class TagRepository(SQLAlchemyAsyncRepository[TagModel]):
    """Tag repository"""

    model_type = TagModel
