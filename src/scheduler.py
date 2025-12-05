from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src import log
from src.digests.dependencies import get_digest_service
from src.digests.models import DigestType
from src.digests.schemas import DigestCreate
from src.sources.dependencies import get_source_service

scheduler = AsyncIOScheduler()


async def create_daily_digests(delta_hours: int) -> None:
    log.info("Creating daily digest")
    source_service = await get_source_service()
    service = await get_digest_service()
    sources = await source_service.get_active_sources()
    for source in sources:
        try:
            digest_data = DigestCreate(
                type=DigestType.DAILY,
                start_time=datetime.now(timezone.utc) - timedelta(hours=delta_hours),
                end_time=datetime.now(timezone.utc),
                source_id=source.id,
                to_chat_id=source.chat_id,
            )
            await service.create_digest(digest_data)

        except Exception as e:
            log.error(f"Create digest error: {str(e)}")


def add_default_jobs() -> None:
    scheduler.add_job(
        create_daily_digests,
        args=(16,),
        trigger=CronTrigger(hour=7, minute=0),
        id="morning_digest_task",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        create_daily_digests,
        args=(8,),
        trigger=CronTrigger(hour=15, minute=0),
        id="evening_digest_task",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
