from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up the application...")
    yield
    log.info("Shutting down the application...")
