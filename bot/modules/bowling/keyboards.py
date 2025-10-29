from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import BowlingCallbackData


def get_bowling_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Страйк (x6)", callback_data=BowlingCallbackData(bet="strike"))
    builder.button(text="Мимо (x6)", callback_data=BowlingCallbackData(bet="miss"))
    builder.button(text="⬅️ Назад в меню", callback_data="play")
    builder.adjust(2)
    return builder.as_markup()
