import json

from advanced_alchemy.extensions.fastapi import service

from .rabbit_routes import publish_new_digest
from .. import log
from ..api.ai import OllamaClient
from ..api.ai.promts import CREATE_DIGEST_PROMPT
from ..storylines.models import StorylineModel
from .models import DigestModel, DigestType
from .repositories import DigestRepository
from .schemas import DigestCreate, Digest
from ..storylines.services import StorylineService


class DigestService(service.SQLAlchemyAsyncRepositoryService[DigestModel, DigestRepository]):
    """Digest Service"""

    repository_type = DigestRepository

    def __init__(self, session, **kwargs):
        kwargs.setdefault("auto_commit", True)
        super().__init__(session=session, **kwargs)
        self._storyline_service = StorylineService(session=session)

    async def create_digest(self, digest: DigestCreate) -> DigestModel:
        storylines = await self._storyline_service.list(
            StorylineModel.start_time >= digest.start_time,
            StorylineModel.end_time <= digest.end_time,
        )
        ollama_client = OllamaClient(system_prompt=CREATE_DIGEST_PROMPT)

        message = json.dumps(
            [
                {
                    "start_time": storyline.start_time.isoformat(),
                    "end_time": storyline.end_time.isoformat(),
                    "summary": storyline.summary,
                    "title": storyline.title,
                }
                for storyline in storylines
            ]
        )
        log.debug("Ollama request", message=message)

        try:
            result = await ollama_client.chat(content=message)
            log.debug("Ollama response", result=result)
            result_json = json.loads(result)
            if "title" not in result_json or "summary" not in result_json:
                raise ValueError()
        except json.JSONDecodeError as e:
            log.error(f"Error decoding JSON response from Ollama: {str(e)}")
            raise
        except ValueError:
            log.error("Unexpected response format from Ollama")
            raise
        except Exception as e:
            log.error(f"Error communicating with Ollama: {str(e)}")
            raise

        new_digest = DigestModel(
            title=result_json["title"],
            summary=result_json["summary"],
            start_time=digest.start_time,
            end_time=digest.end_time,
            type=digest.type,
            storylines=list(storylines),
        )
        new_digest = await self.create(new_digest)

        log.info("New digest", digest=new_digest.to_dict())

        if digest.type == DigestType.DAILY:
            tags = await self.repository.get_tags(new_digest.id)
            digest = Digest(
                **new_digest.to_dict(),
                tags=[tag.model_dump() for tag in tags],
            )
            await publish_new_digest(digest)

        return new_digest
