from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from .models import StorylineModel


class StorylineRepository(SQLAlchemyAsyncRepository[StorylineModel]):
    """Storyline repository"""

    model_type = StorylineModel
