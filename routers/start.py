from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from database.database import async_session
from database.models import User
from keyboards.geoposition import create_geo_keyboard

start_router = Router()


@start_router.message(F.text == '/start')
async def start(message: Message):
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if user:
            return
    await message.answer(
        text=f'Привет, <b>{message.from_user.first_name}</b>! Отправь свою геопозицию и получай информацию о погоде',
        reply_markup=create_geo_keyboard()
    )


@start_router.message(F.text == '/remove_keyboard')
async def remove_keyboard(message: Message):
    await message.answer('Клавиатура убрана.', reply_markup=ReplyKeyboardRemove())
