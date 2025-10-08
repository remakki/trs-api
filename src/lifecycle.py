from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import log
from src.scheduler import add_default_jobs, scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting application...")
    log.info("Starting scheduler...")
    scheduler.start()
    add_default_jobs()
    log.info("Scheduler started")
    log.info("Application started")

    yield
    log.info("Shutting down application...")
    log.info("Stopping scheduler...")
    scheduler.shutdown()
    log.info("Scheduler stopped")
    log.info("Application shut down")
