from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import extract_dates_from_forecastday


def create_inline_date_weather_keyboard(forecastday: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for date in extract_dates_from_forecastday(forecastday):
        builder.add(InlineKeyboardButton(text=date, callback_data=f'date: {date}'))
    builder.adjust(4)
    return builder.as_markup()


def create_inline_hour_weather_keyboard(day_num: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for hour in range(0, 24):
        builder.add(InlineKeyboardButton(text=f'{hour}:00', callback_data=f'hour: {hour}: {day_num}'))
    builder.add(InlineKeyboardButton(text='Общая информация', callback_data=f'date: {day_num}'))
    builder.add(InlineKeyboardButton(text='Все дни', callback_data='weather'))
    builder.adjust(6)
    return builder.as_markup()
