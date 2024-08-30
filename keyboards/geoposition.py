from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def create_geo_keyboard(geo: bool = False):
    keyboard = [[KeyboardButton(text='📍 Установить геопозицию', request_location=True)]]
    if geo:
        keyboard.append([KeyboardButton(text='❌ Удалить геопозицию')])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие...'
    )
