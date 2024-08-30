import datetime

from aiogram.types import BotCommand
from sqlalchemy import select
from json import dumps
from database.database import async_session
from database.models import User
from mappings import condition, WindDirections
from builder import bot, weather_api, redis


async def set_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Старт бота'),
            BotCommand(command='geo', description='Просмотр и изменение геопозиции'),
            BotCommand(command='notifications', description='Настройка уведомлений'),
            BotCommand(command='weather', description='Просмотреть погоду'),
        ]
    )


def cache_weather(q: str, return_key: bool = False) -> str | None:
    information = weather_api.forecast_weather(q, days=14)
    redis.set(information['location']['name'], dumps(information['forecast']['forecastday']), ex=86400)
    return information['location']['name'] if return_key else None


async def cache_all_weather() -> None:
    async with async_session() as session:
        locations = tuple((await session.scalars(select(User.location))).all())
    for q in locations:
        cache_weather(q)


def format_fully(hour: dict) -> str:
    return (
        f'<b>Время:</b> {hour["time"]}\n'
        f'<b>Температура:</b> {hour["temp_c"]}°C (ощущается как {hour["feelslike_c"]}°C) /'
        f' {hour["temp_f"]}°F (ощущается как {hour["feelslike_f"]}°F)\n'
        f'<b>Ветер:</b> скорость {hour["wind_kph"]} км/ч, направление {WindDirections[hour["wind_dir"]].value}, '
        f'порывы до {hour["gust_kph"]} км/ч\n'
        f'<b>Давление:</b> {hour["pressure_mb"]} мбар\n'
        f'<b>Влажность:</b> {hour["humidity"]}%\n'
        f'<b>Облачность:</b> {hour["cloud"]}%\n'
        f'<b>Осадки:</b> {hour["precip_mm"]} мм\n'
        f'<b>Точка росы:</b> {hour["dewpoint_c"]}°C / {hour["dewpoint_f"]}°F\n'
        f'<b>Видимость:</b> {hour["vis_km"]} км\n'
        f'<b>УФ-индекс:</b> {hour["uv"]}\n'
        f'<b>Состояние:</b> {condition[hour["condition"]["code"]]}\n'
    )


def format_partly(day: dict) -> str:
    return (
        f'<b>Дата:</b> {day["date"]}\n'
        f'<b>Максимальная температура:</b> {day["day"]["maxtemp_c"]}°C / {day["day"]["maxtemp_f"]}°F\n'
        f'<b>Минимальная температура:</b> {day["day"]["mintemp_c"]}°C / {day["day"]["mintemp_f"]}°F\n'
        f'<b>Средняя температура:</b> {day["day"]["avgtemp_c"]}°C / {day["day"]["avgtemp_f"]}°F\n'
        f'<b>Максимальный ветер:</b> {day["day"]["maxwind_kph"]} км/ч\n'
        f'<b>Средняя влажность:</b> {day["day"]["avghumidity"]}%\n'
        f'<b>Состояние:</b> {condition[day["day"]["condition"]["code"]]}\n'
        f'<b>УФ-индекс:</b> {day["day"]["uv"]}\n'
    )


def extract_dates_from_forecastday(forecastday: list[dict]) -> list:
    dates = []
    for day in forecastday:
        dates.append(day['date'])
    return dates


def make_associations_dict(today: datetime.date):
    date_associations = {}
    current_date = today
    current_number = 1
    date_associations[current_date.strftime('%Y-%m-%d')] = current_number
    for i in range(1, 14):
        current_date += datetime.timedelta(days=1)
        current_number += 1
        date_associations[current_date.strftime('%Y-%m-%d')] = current_number
    return date_associations
