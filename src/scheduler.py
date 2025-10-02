from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src import log
from src.digests.dependencies import get_digest_service
from src.digests.models import DigestType
from src.digests.schemas import DigestCreate

scheduler = AsyncIOScheduler()


async def create_daily_digest(delta_hours: int) -> None:
    log.info("Creating daily digest")
    try:
        service = await get_digest_service()

        digest_data = DigestCreate(
            type=DigestType.DAILY,
            start_time=datetime.now(timezone.utc) - timedelta(hours=delta_hours),
            end_time=datetime.now(timezone.utc),
        )

        await service.create_digest(digest_data)

    except Exception as e:
        log.error(f"Ошибка при создании автоматического дайджеста: {str(e)}")


def add_default_jobs() -> None:
    scheduler.add_job(
        create_daily_digest,
        args=(16,),
        trigger=CronTrigger(hour=10, minute=0),
        id="morning_digest_task",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        create_daily_digest,
        args=(8,),
        trigger=CronTrigger(hour=18, minute=0),
        id="evening_digest_task",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
