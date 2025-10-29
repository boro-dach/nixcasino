# dice/keyboards.py
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import DiceCallbackData


def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎲 Один бросок",
        callback_data=DiceCallbackData(game_mode="single", bet="menu"),
    )
    builder.button(
        text="🎲🎲 Два броска",
        callback_data=DiceCallbackData(game_mode="double", bet="menu"),
    )
    builder.button(
        text="🎲 x 🎲 Произведение",
        callback_data=DiceCallbackData(game_mode="multiply", bet="menu"),
    )
    builder.button(
        text="🎲 + 🎲 Сумма +-7",
        callback_data=DiceCallbackData(game_mode="plus_minus_7", bet="menu"),
    )
    builder.button(
        text="🎯 На число",
        callback_data=DiceCallbackData(game_mode="specific_number", bet="menu"),
    )
    builder.adjust(1)
    return builder.as_markup()


def get_single_throw_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Четное (x2)",
        callback_data=DiceCallbackData(game_mode="single", bet="even"),
    )
    builder.button(
        text="Нечетное (x2)",
        callback_data=DiceCallbackData(game_mode="single", bet="odd"),
    )
    builder.button(
        text="Больше 3 (x2)",
        callback_data=DiceCallbackData(game_mode="single", bet="more"),
    )
    builder.button(
        text="Меньше 4 (x2)",
        callback_data=DiceCallbackData(game_mode="single", bet="less"),
    )
    builder.button(
        text="⬅️ Назад", callback_data=DiceCallbackData(game_mode="main", bet="menu")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_double_throw_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Оба четные (x3.8)",
        callback_data=DiceCallbackData(game_mode="double", bet="both_even"),
    )
    builder.button(
        text="Оба нечетные (x3.8)",
        callback_data=DiceCallbackData(game_mode="double", bet="both_odd"),
    )
    builder.button(
        text="Две 6 (x36)",
        callback_data=DiceCallbackData(game_mode="double", bet="two_six"),
    )
    builder.button(
        text="Дубль (x5.7)",
        callback_data=DiceCallbackData(game_mode="double", bet="double"),
    )
    builder.button(
        text="Сумма четная (x1.9)",
        callback_data=DiceCallbackData(game_mode="double", bet="sum_even"),
    )
    builder.button(
        text="Сумма нечетная (x1.9)",
        callback_data=DiceCallbackData(game_mode="double", bet="sum_odd"),
    )
    builder.button(
        text="⬅️ Назад", callback_data=DiceCallbackData(game_mode="main", bet="menu")
    )
    builder.adjust(2)
    return builder.as_markup()


def get_multiply_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="1 - 18 (x1.2)",
        callback_data=DiceCallbackData(game_mode="multiply", bet="1_18"),
    )
    builder.button(
        text="18 - 36 (x4.2)",
        callback_data=DiceCallbackData(game_mode="multiply", bet="18_36"),
    )
    builder.button(
        text="⬅️ Назад", callback_data=DiceCallbackData(game_mode="main", bet="menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_plus_minus_7_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Больше 7 (x2.4)",
        callback_data=DiceCallbackData(game_mode="plus_minus_7", bet="more_7"),
    )
    builder.button(
        text="Точно 7 (x6)",
        callback_data=DiceCallbackData(game_mode="plus_minus_7", bet="equal_7"),
    )
    builder.button(
        text="Меньше 7 (x2.4)",
        callback_data=DiceCallbackData(game_mode="plus_minus_7", bet="less_7"),
    )
    builder.button(
        text="⬅️ Назад", callback_data=DiceCallbackData(game_mode="main", bet="menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_specific_number_keyboard():
    builder = InlineKeyboardBuilder()
    for i in range(1, 7):
        builder.button(
            text=f"{i} (x5)",
            callback_data=DiceCallbackData(game_mode="specific_number", bet=str(i)),
        )
    builder.button(
        text="⬅️ Назад", callback_data=DiceCallbackData(game_mode="main", bet="menu")
    )
    builder.adjust(3)
    return builder.as_markup()
