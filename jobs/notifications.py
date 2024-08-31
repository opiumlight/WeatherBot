from json import loads
from sqlalchemy import select
from builder import bot, r
from database.database import async_session
from database.models import User
from utils import format_partly


async def send_today_weather(user: User) -> None:
    await bot.send_message(
        chat_id=user.id,
        text=f'Привет, погода на сегодня:\n\n{format_partly(loads(r.get(user.location))[0])}'
    )


async def newsletter() -> None:
    async with async_session() as session:
        users = (await session.scalars(select(User))).all()
    for user in users:
        if user.notifications:
            await send_today_weather(user)
