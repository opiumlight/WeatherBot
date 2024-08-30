import asyncio
from apscheduler.triggers.cron import CronTrigger
from builder import bot, dp, scheduler
from database.database import engine
from jobs.notifications import newsletter
from routers import routers_list
from utils import set_commands, cache_all_weather
from database.models import Base


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scheduler.add_job(cache_all_weather, CronTrigger(hour=0, minute=0))
    scheduler.add_job(newsletter, CronTrigger(hour=0, minute=0))  # TODO: Make personal notifications
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(*routers_list)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())
