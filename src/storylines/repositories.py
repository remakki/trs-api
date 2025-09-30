from typing import Iterable

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy import select

from .models import StorylineModel
from ..tags.models import TagModel


class StorylineRepository(SQLAlchemyAsyncRepository[StorylineModel]):
    """Storyline repository"""

    model_type = StorylineModel
