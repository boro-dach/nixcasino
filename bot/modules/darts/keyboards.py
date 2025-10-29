from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import DartsCallbackData


def get_darts_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Красный сектор (x2)", callback_data=DartsCallbackData(bet="red")
    )
    builder.button(
        text="Белый сектор (x2.5)", callback_data=DartsCallbackData(bet="white")
    )
    builder.button(text="Промах (x5)", callback_data=DartsCallbackData(bet="miss"))
    builder.button(text="Центр (x5)", callback_data=DartsCallbackData(bet="center"))
    builder.button(text="⬅️ Назад в меню", callback_data="play")
    builder.adjust(2)
    return builder.as_markup()
