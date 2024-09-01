from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from builder import scheduler
from jobs.notifications import add_notifications_jobs
from utils import cache_all_weather


async def run_jobs():
    scheduler.add_job(cache_all_weather, CronTrigger(hour=0, minute=0), next_run_time=datetime.now())
    await add_notifications_jobs()
    scheduler.start()
