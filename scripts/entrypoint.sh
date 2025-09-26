#!/bin/bash
set -e

./scripts/wait-for-it.sh "$DB_HOST:$DB_PORT" -- echo "Postgres is up - running migrations..."

uv run alembic upgrade head

exec "$@"
