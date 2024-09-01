from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def create_inline_notifications_keyboard(is_on: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_on:
        builder.add(InlineKeyboardButton(text='Изменить время', callback_data='change'))
        builder.add(InlineKeyboardButton(text='✖ Выключить уведомления', callback_data='False'))
    else:
        builder.add(InlineKeyboardButton(text='✔ Включить уведомления', callback_data='True'))
    return builder.as_markup()


def create_inline_wish_to_change_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Да', callback_data='change'))
    builder.add(InlineKeyboardButton(text='Нет', callback_data='keep'))
    return builder.as_markup()


def create_inline_hour_selection_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(0, 24):
        builder.add(InlineKeyboardButton(text=str(i), callback_data=f'time_select_1:{i}'))
    builder.add(InlineKeyboardButton(text='Назад', callback_data='keep'))
    return builder.as_markup()


def create_inline_minute_selection_keyboard(hour: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(0, 61):
        builder.add(InlineKeyboardButton(text=str(i), callback_data=f'time_select_2:{hour}:{i}'))
    builder.add(InlineKeyboardButton(text='Назад', callback_data='change'))
    return builder.as_markup()
