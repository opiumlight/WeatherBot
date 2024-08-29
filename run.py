import asyncio
from builder import bot, dp, scheduler


async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    # await set_commands()

if __name__ == "__main__":
    asyncio.run(main())
