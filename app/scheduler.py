import json
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.questions import (
    add_daily_question_to_mongodb,
    generate_daily_question,
)
from app.utils.generic_functions import execute_with_retries

logger = logging.getLogger(__name__)


class SchedulerManager:
    """Manages the APScheduler instance and scheduled jobs."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.job = None

    # TODO/question: should we raise error if job fails after retries?
    async def _generate_and_store_daily_question(self):
        """Generate a daily question and store it in MongoDB."""
        try:
            question = generate_daily_question()
            question_json = json.loads(question)
            add_daily_question_to_mongodb(question_json)
        except (json.JSONDecodeError, TypeError, RuntimeError) as e:
            logger.error("Error running schedul daily job: %s", e)
        except BaseException as e:
            logger.error("Unexpected critical error: %s", e)

    async def _daily_question_task(self):
        """Wrapper to execute the daily question generation with retries."""
        await execute_with_retries(
            self._generate_and_store_daily_question, max_retries=3, delay=5
        )

    def start(self, interval_hour: int):
        """Start the scheduler and add the daily question job."""
        try:
            self.job = self.scheduler.add_job(
                self._daily_question_task,
                "interval",
                minutes=1,
                id="daily_question_job",
                replace_existing=True,
            )
            self.scheduler.start()
            logger.info(
                "Scheduler started successfully with interval %d hour.", interval_hour
            )
        except Exception as e:
            logger.error("Error starting scheduler: %s", e)
            raise e

    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
        logger.info("Scheduler shutdown completed.")


# Singleton instance for use in FastAPI app
scheduler_manager = SchedulerManager()


def start_scheduler():
    """Start the scheduler with a 1-minute interval for testing purposes."""
    scheduler_manager.start(interval_hour=24)


def shutdown_scheduler():
    """Shutdown the scheduler."""
    scheduler_manager.shutdown()
