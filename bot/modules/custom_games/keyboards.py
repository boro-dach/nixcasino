from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import CustomGameCallbackData


def get_custom_game_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Число от 1 до 20 (x3)", callback_data=CustomGameCallbackData(bet="1_20")
    )
    builder.button(
        text="Число от 21 до 40 (x3)", callback_data=CustomGameCallbackData(bet="21_40")
    )
    builder.button(
        text="Число от 41 до 60 (x3)", callback_data=CustomGameCallbackData(bet="41_60")
    )
    builder.button(
        text="🔥 Джекпот! (61-64) (x15)",
        callback_data=CustomGameCallbackData(bet="jackpot"),
    )
    builder.button(text="⬅️ Назад в меню", callback_data="play")
    builder.adjust(1)
    return builder.as_markup()
