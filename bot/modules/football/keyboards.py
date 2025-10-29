from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import FootballCallbackData


def get_football_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Гол (x1.6)", callback_data=FootballCallbackData(bet="goal"))
    builder.button(text="Промах (x2.5)", callback_data=FootballCallbackData(bet="miss"))
    builder.button(text="⬅️ Назад", callback_data="play")
    builder.adjust(2)
    return builder.as_markup()
