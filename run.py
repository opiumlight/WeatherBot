import asyncio
from builder import bot, dp, scheduler
from database.database import engine
from routers import routers_list
from utils import set_commands, cache_all_weather
from database.models import Base


async def main():
    await cache_all_weather()
    scheduler.add_job(cache_all_weather, 'interval', days=1)
    scheduler.start()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    dp.include_routers(*routers_list)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())
