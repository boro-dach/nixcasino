from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import BasketballCallbackData


def get_basketball_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Чистый гол (x5)", callback_data=BasketballCallbackData(bet="clean_goal")
    )
    builder.button(
        text="Любой гол (x2.5)", callback_data=BasketballCallbackData(bet="any_goal")
    )
    builder.button(
        text="Застрял мяч (x5)", callback_data=BasketballCallbackData(bet="stuck")
    )
    builder.button(
        text="Промах (x1.6)", callback_data=BasketballCallbackData(bet="miss")
    )
    builder.button(text="⬅️ Назад", callback_data="play")
    builder.adjust(2)
    return builder.as_markup()
