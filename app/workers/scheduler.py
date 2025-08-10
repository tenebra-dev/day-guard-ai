import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self) -> None:
        logger.info("Starting scheduler...")
        self.scheduler.start()

    def shutdown(self) -> None:
        logger.info("Shutting down scheduler...")
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def add_daily_summary(self, hour: int = 18, minute: int = 0) -> None:
        logger.info("Adding daily summary job at %02d:%02d", hour, minute)
        self.scheduler.add_job(self._daily_summary_job, CronTrigger(hour=hour, minute=minute))

    @staticmethod
    def _daily_summary_job() -> None:
        logger.info("Running daily summary job...")
        # TODO: collect context and call AIService.summarize
