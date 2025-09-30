import json

from advanced_alchemy.extensions.fastapi import service

from .models import DigestModel, DigestType
from .publisher import publish_new_digest
from .repositories import DigestRepository
from .schemas import DigestCreate, DigestTag
from .. import log
from ..api.ai import OllamaClient
from ..api.ai.promts import CREATE_DIGEST_PROMPT
from ..storylines.dependencies import get_storyline_service
from ..storylines.models import StorylineModel


class DigestService(service.SQLAlchemyAsyncRepositoryService[DigestModel, DigestRepository]):
    """Digest Service"""

    repository_type = DigestRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)

    async def create_digest(self, digest: DigestCreate) -> DigestModel:
        storyline_service = await get_storyline_service()
        storylines = await storyline_service.list(
            StorylineModel.start_time >= digest.start_time,
            StorylineModel.end_time <= digest.end_time,
        )
        ollama_client = OllamaClient(system_prompt=CREATE_DIGEST_PROMPT)

        message = json.dumps(
            [
                {
                    "start_time": storyline.start_time,
                    "end_time": storyline.end_time,
                    "summary": storyline.summary
                }
                for storyline in storylines
            ]
        )

        try:
            result = await ollama_client.chat(content=message)
            result_json = json.loads(result)
            if 'title' not in result_json or 'summary' not in result_json:
                raise ValueError("Некорректный формат ответа от Ollama")
        except json.JSONDecodeError as e:
            log.error(f"Ошибка при разборе JSON от Ollama: {str(e)}")
            raise
        except ValueError as e:
            log.error("Некорректный формат ответа от Ollama")
            raise
        except Exception as e:
            log.error(f"Ошибка при создании дайджеста с помощью Ollama: {str(e)}")
            raise

        new_digest = DigestModel(
            title=result_json['title'],
            summary=result_json['summary'],
            start_time=digest.start_time,
            end_time=digest.end_time,
            type=digest.type,
            storylines=list(storylines),
        )
        new_digest = await self.create(new_digest)

        log.info(f"Новый дайджест", digest=new_digest.to_dict())

        if digest.type == DigestType.DAILY:
            tags = await self.repository.get_tags(new_digest.id)
            await publish_new_digest(new_digest, tags)

        return new_digest
