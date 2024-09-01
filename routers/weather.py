from json import loads

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, ErrorEvent
from sqlalchemy import select
import datetime

from builder import r
from database.database import async_session
from database.models import User
from keyboards.geoposition import create_geo_keyboard
from keyboards.weather import create_inline_hour_weather_keyboard, create_inline_date_weather_keyboard
from utils import make_associations_dict, format_partly, format_fully

weather_router = Router()


@weather_router.message(F.text == '/weather')
async def weather(message: Message):
    async with async_session() as session:
        location = await session.scalar(select(User.location).filter_by(id=message.from_user.id))
    if location:
        answer = 'Выберите, погоду на какой день вы хотите посмотреть.'
        reply_markup = create_inline_date_weather_keyboard(loads(r.get(location)))
    else:
        answer = 'Вы не указали свою геопозицию.'
        reply_markup = create_geo_keyboard()
    await message.answer(answer, reply_markup=reply_markup)


@weather_router.callback_query(F.data == 'weather')
async def weather_callback(callback: CallbackQuery):
    async with async_session() as session:
        location = await session.scalar(select(User.location).filter_by(id=callback.from_user.id))
    await callback.message.edit_text(
        'Выберите, погоду на какой день вы хотите посмотреть.',
        reply_markup=create_inline_date_weather_keyboard(loads(r.get(location)))
    )


@weather_router.callback_query(F.data.split(':')[0] == 'date')
async def date(callback: CallbackQuery):
    associations = make_associations_dict(datetime.date.today())
    async with async_session() as session:
        user = await session.scalar(select(User).filter_by(id=callback.from_user.id))
    date_or_day_num = callback.data.split(':')[1]
    day_num = associations[date_or_day_num] - 1 if len(date_or_day_num) > 2 else int(date_or_day_num)
    day = loads(r.get(user.location))[day_num]
    await callback.message.edit_text(
        text=format_partly(day),
        reply_markup=create_inline_hour_weather_keyboard(day_num)
    )


@weather_router.callback_query(F.data.split(':')[0] == 'hour')
async def hour(callback: CallbackQuery):
    day_num = int(callback.data.split(':')[2])
    async with async_session() as session:
        user = await session.scalar(select(User).filter_by(id=callback.from_user.id))
    await callback.message.edit_text(
        text=format_fully(loads(r.get(user.location))[day_num]['hour'][int(callback.data.split(':')[1])]),
        reply_markup=create_inline_hour_weather_keyboard(day_num)
    )


@weather_router.errors()
async def error_handler(event: ErrorEvent):
    if isinstance(event.exception, TelegramBadRequest):
        await event.update.callback_query.answer()
    raise event.exception
