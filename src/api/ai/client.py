import asyncio

import ollama
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings


class OllamaClient:
    def __init__(self, system_prompt: str, model: str | None = None) -> None:
        self._client = ollama.AsyncClient(
            host=settings.OLLAMA_BASE_URL,
            headers={"Authorization": f"Bearer {settings.OLLAMA_TOKEN}"},
        )
        self._model = model or settings.OLLAMA_MODEL
        self._system_prompt = system_prompt

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def chat(self, content: str, timeout: float = 300.0) -> str:
        answer = await asyncio.wait_for(
            self._client.chat(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": f"{self._system_prompt}\n\nList of news segments:\n{content}",
                    }
                ],
                format="json",
                options={
                    "temperature": 0.7,
                    "seed": 42,
                },
            ),
            timeout=timeout,
        )
        return answer["message"]["content"]
