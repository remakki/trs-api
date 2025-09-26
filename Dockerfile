FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY uv.lock pyproject.toml ./

RUN uv sync

COPY . .

RUN chmod +x ./scripts/entrypoint.sh ./scripts/wait-for-it.sh

ENTRYPOINT ["./scripts/entrypoint.sh"]

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
