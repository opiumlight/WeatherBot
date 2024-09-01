from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update, insert, delete
from database.database import async_session
from database.models import User
from database.models import Notification
from jobs.notifications import add_notification_job
from keyboards.geoposition import create_geo_keyboard
from keyboards.notifications import (
    create_inline_notifications_keyboard,
    create_inline_wish_to_change_keyboard,
    create_inline_hour_selection_keyboard,
    create_inline_minute_selection_keyboard
)

notifications_router = Router()


@notifications_router.message(F.text == '/notifications')
async def notifications(message: Message):
    async with async_session() as session:
        if not await session.scalar(select(User).filter_by(id=message.from_user.id)):
            await message.answer(text='У вас нет геопозиции!', reply_markup=create_geo_keyboard())
            return
        result = (await session.execute(
            select(Notification.hour, Notification.minute).filter_by(user_id=message.from_user.id)
        )).fetchone()
    if result:
        hour, minute = result
    else:
        hour, minute = None, None
    time = None
    if isinstance(hour, int):
        time = f'{hour if hour > 9 else f"0{hour}"}:{minute if minute > 9 else f"0{minute}"}'
    is_on = isinstance(time, str)
    await message.answer(
        text=f'Уведомления стоят на {time}' if is_on else 'Уведомления выключены.',
        reply_markup=create_inline_notifications_keyboard(is_on=is_on)
    )


@notifications_router.callback_query(F.data.in_({'True', 'False'}))
async def turn_notifications(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(select(User).filter_by(id=callback.from_user.id))
        if str(user.notifications) == callback.data:
            await callback.answer(text='У вас уже данная настройка.')
            return
        await session.execute(update(User).values(notifications=True if callback.data == 'True' else False))
        if callback.data == 'True':
            await session.execute(insert(Notification).values(user_id=user.id, minute=0, hour=0))
            text = 'Уведомления включены на 00:00. Хотите изменить время?'
            reply_markup = create_inline_wish_to_change_keyboard()
        else:
            await session.execute(delete(Notification).filter_by(user_id=user.id))
            text = 'Уведомления выключены.'
            reply_markup = None
        await session.commit()
    await callback.message.edit_text(text, reply_markup=reply_markup)


@notifications_router.callback_query(F.data.in_({'change', 'keep'}))
async def turn_notification_time(callback: CallbackQuery):
    if callback.data == 'keep':
        async with async_session() as session:
            n = await session.scalar(select(Notification).filter_by(user_id=callback.from_user.id))
            user = await session.scalar(select(User).filter_by(id=callback.from_user.id))
        add_notification_job(n, user)
        time = f'{n.hour if n.hour > 9 else f"0{n.hour}"}:{n.minute if n.minute > 9 else f"0{n.minute}"}'
        await callback.message.edit_text(f'Отлично! Уведомления будут приходить каждый день в {time}.')
        return
    await callback.message.edit_text(
        'Выберите в какой час дня будет приходить уведомление: ',
        reply_markup=create_inline_hour_selection_keyboard()
    )


@notifications_router.callback_query(F.data.split(':')[0] == 'time_select_1')
async def turn_notification_hour(callback: CallbackQuery):
    await callback.message.edit_text(
        f'Хорошо, теперь выберите минуту (выбран час {callback.data.split(":")[1]}): ',
        reply_markup=create_inline_minute_selection_keyboard(int(callback.data.split(':')[1]))
    )


@notifications_router.callback_query(F.data.split(':')[0] == 'time_select_2')
async def turn_notification_minute(callback: CallbackQuery):
    hour, minute = map(int, callback.data.split(':')[1:])
    async with async_session() as session:
        n = await session.scalar(
            update(Notification)
            .values(hour=hour, minute=minute)
            .filter_by(user_id=callback.from_user.id)
            .returning(Notification)
        )
        user = await session.get(User, callback.from_user.id)
        await session.commit()
    add_notification_job(n, user)
    time = f'{hour if hour > 9 else f"0{hour}"}:{minute if minute > 9 else f"0{minute}"}'
    await callback.message.edit_text(f'Отлично! Уведомления будут приходить каждый день в {time}.')
