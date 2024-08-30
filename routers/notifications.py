from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from database.database import async_session
from database.models import User
from keyboards.notifications import create_inline_notifications_keyboard

notifications_router = Router()


@notifications_router.message(F.text == '/notifications')
async def notifications(message: Message):
    await message.answer(
        text=f'Настройки уведомлений.',
        reply_markup=create_inline_notifications_keyboard()
    )


@notifications_router.callback_query(F.data.in_({'True', 'False'}))
async def turn_notifications(callback: CallbackQuery):
    async with async_session() as session:
        user = await session.scalar(select(User).filter_by(id=callback.from_user.id))
        if str(user.notifications) == callback.data:
            await callback.answer(text='У вас уже данная настройка.', show_alert=True)
            return
        await session.execute(update(User).values(notifications=True if callback.data == 'True' else False))
        await session.commit()
    await callback.message.edit_text('Уведомления включены.' if callback.data == 'True' else 'Уведомления выключены.')
