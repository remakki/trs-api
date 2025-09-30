import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import log
from src.mq import broker, faststream
from src.scheduler import scheduler, add_default_jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting application...")
    log.info("Connecting to the message broker...")
    await broker.start()
    log.info("Broker connected")
    log.info("Starting scheduler...")
    scheduler.start()
    add_default_jobs()
    log.info("Scheduler started")

    log.info("Starting FastStream...")
    task = asyncio.create_task(faststream.run())
    log.info("FastStream started")
    log.info("Application started")

    yield
    log.info("Shutting down application...")
    log.info("Stopping scheduler...")
    scheduler.shutdown()
    log.info("Scheduler stopped")
    log.info("Stopping FastStream...")
    task.cancel()
    log.info("✓ FastStream stopped")
    await broker.close()
    log.info("✓ Broker closed")
    log.info("✓ Application shut down")
