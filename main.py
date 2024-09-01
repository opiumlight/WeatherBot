import asyncio
from builder import bot, dp
from jobs.run import run_jobs
from database.database import create_tables
from routers import routers_list
from utils import set_commands


async def main():
    await create_tables()
    await run_jobs()
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_routers(*routers_list)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())
