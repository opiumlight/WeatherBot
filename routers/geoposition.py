from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import IntegrityError

from database.database import async_session
from database.models import User
from keyboards.geoposition import create_geo_keyboard
from utils import cache_weather

geo_router = Router()


@geo_router.message(F.text == '/geo')
async def geo(message: Message):
    async with async_session() as session:
        user = await session.scalar(select(User).filter_by(id=message.from_user.id))
    await message.answer(
        f'Ваша геопозиция: {user.lat}, {user.lon} ({user.location}).' if user else 'У вас нет геопозиции.',
        reply_markup=create_geo_keyboard(geo=True if user else False)
    )


@geo_router.message(F.text == '❌ Удалить геопозицию')
async def delete_geo(message: Message):
    async with async_session() as session:
        await session.execute(delete(User).filter_by(id=message.from_user.id))
        await session.commit()
    await message.answer(
        'Вы успешно удалили геопозицию. Уведомления о погоде более не будут приходить.',
        reply_markup=ReplyKeyboardRemove()
    )


@geo_router.message(F.location)
async def handle_location(message: Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    key = cache_weather(f'{latitude},{longitude}', return_key=True)
    async with async_session() as session:
        try:
            await session.execute(
                insert(User).values(
                    id=message.from_user.id,
                    lat=latitude,
                    lon=longitude,
                    location=key
                )
            )
        except IntegrityError:
            await session.rollback()
            await session.execute(
                update(User).values(lat=latitude, lon=longitude, location=key).filter_by(id=message.from_user.id)
            )
        await session.commit()
    await message.answer(
        f'Вы обновили геопозицию на: {latitude}, {longitude} ({key}).',
        reply_markup=ReplyKeyboardRemove()
    )
