from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def create_inline_notifications_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='✔ Включить уведомления', callback_data='True'))
    builder.add(InlineKeyboardButton(text='✖ Выключить уведомления', callback_data='False'))
    return builder.as_markup()
