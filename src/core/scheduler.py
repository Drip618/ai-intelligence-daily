from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from src.core.agent import IntelligenceAgent


class AgentScheduler:
    """Scheduler for running agent routines."""

    def __init__(self, agent: IntelligenceAgent, cron_expr: str = "0 9 * * *", timezone: str = "Asia/Shanghai"):
        self.agent = agent
        self.scheduler = BlockingScheduler(timezone=timezone)
        self.cron_expr = cron_expr

        parts = cron_expr.split()
        minute, hour, day, month, day_of_week = parts
        self.trigger = CronTrigger(
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            day_of_week=day_of_week,
            timezone=timezone,
        )

    def start(self):
        """Start the scheduler."""
        self.scheduler.add_job(
            self.agent.run_daily_routine,
            self.trigger,
            id="daily_intelligence_routine",
            name="Daily AI Intelligence Collection",
            replace_existing=True,
        )
        logger.info(f"Scheduled daily routine with cron: {self.cron_expr}")
        logger.info("Starting scheduler...")
        self.scheduler.start()

    def stop(self):
        """Stop the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
