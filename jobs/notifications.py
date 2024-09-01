from json import loads
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import select

from builder import bot, r, scheduler
from database.database import async_session
from database.models import User
from database.models import Notification
from utils import format_partly


async def send_today_weather(user: User) -> None:
    await bot.send_message(
        chat_id=user.id,
        text=f'Привет, погода на сегодня:\n\n{format_partly(loads(r.get(user.location))[0])}'
    )


def add_notification_job(n: Notification, user: User) -> None:
    if scheduler.get_job(f'user_{user.id}'):
        scheduler.remove_job(f'user_{user.id}')
    scheduler.add_job(
        send_today_weather,
        CronTrigger(hour=n.hour, minute=n.minute),
        args=[user],
        name=f'user_{user.id}'
    )


async def add_notifications_jobs() -> None:
    async with async_session() as session:
        notifications = (await session.scalars(select(Notification))).all()
        for n in notifications:
            add_notification_job(n, await session.scalar(select(User).filter_by(id=n.user_id)))
