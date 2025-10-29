import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from .keyboards import (
    get_main_menu_keyboard,
    get_single_throw_keyboard,
    get_double_throw_keyboard,
    get_multiply_keyboard,
    get_plus_minus_7_keyboard,
    get_specific_number_keyboard,
)
from .callback_data import DiceCallbackData

router = Router()


@router.callback_query(F.data == "dice")
async def show_dice_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Добро пожаловать в игру в кости! Выберите режим:",
        reply_markup=get_main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(DiceCallbackData.filter(F.bet == "menu"))
async def navigate_to_menu(callback: CallbackQuery, callback_data: DiceCallbackData):
    keyboards = {
        "main": (get_main_menu_keyboard, "Выберите режим:"),
        "single": (get_single_throw_keyboard, "Один бросок:"),
        "double": (get_double_throw_keyboard, "Два броска:"),
        "multiply": (get_multiply_keyboard, "Произведение двух:"),
        "plus_minus_7": (get_plus_minus_7_keyboard, "Сумма ±7:"),
        "specific_number": (get_specific_number_keyboard, "На число:"),
    }

    keyboard_func, text = keyboards.get(callback_data.game_mode)
    await callback.message.edit_text(text, reply_markup=keyboard_func())
    await callback.answer()


@router.callback_query(DiceCallbackData.filter(F.bet != "menu"))
async def process_bet(callback: CallbackQuery, callback_data: DiceCallbackData):
    await callback.message.edit_text("Ваша ставка принята. Бросаем кости...")
    await callback.answer()
    await asyncio.sleep(1)

    if callback_data.game_mode in ["single", "specific_number"]:
        dice_msg = await callback.message.answer_dice(emoji="🎲")
        await asyncio.sleep(4)  # Даем время на анимацию
        await _process_single_throw(
            callback.message, dice_msg.dice.value, callback_data
        )
    else:
        dice1_msg = await callback.message.answer_dice(emoji="🎲")
        await asyncio.sleep(4)
        dice2_msg = await callback.message.answer_dice(emoji="🎲")
        await asyncio.sleep(4)
        await _process_double_throw(
            callback.message, dice1_msg.dice.value, dice2_msg.dice.value, callback_data
        )


async def _process_single_throw(message: Message, value: int, data: DiceCallbackData):
    result_text = f"🎲 Выпало: {value}\n\n"
    win = False

    if data.game_mode == "single":
        if data.bet == "even" and value % 2 == 0:
            win = True
        if data.bet == "odd" and value % 2 != 0:
            win = True
        if data.bet == "more" and value in {4, 5, 6}:
            win = True
        if data.bet == "less" and value in {1, 2, 3}:
            win = True
    elif data.game_mode == "specific_number":
        if int(data.bet) == value:
            win = True

    result_text += "🎉 Вы победили!" if win else "😔 Вы проиграли."
    await message.answer(result_text, reply_markup=get_main_menu_keyboard())


async def _process_double_throw(
    message: Message, val1: int, val2: int, data: DiceCallbackData
):
    result_text = f"🎲🎲 Выпало: {val1} и {val2}\n"
    win = False
    total = val1 + val2
    product = val1 * val2

    if data.game_mode == "double":
        if data.bet == "both_even" and val1 % 2 == 0 and val2 % 2 == 0:
            win = True
        if data.bet == "both_odd" and val1 % 2 != 0 and val2 % 2 != 0:
            win = True
        if data.bet == "both_more" and val1 > 3 and val2 > 3:
            win = True
        if data.bet == "both_less" and val1 < 4 and val2 < 4:
            win = True
        if data.bet == "two_six" and val1 == 6 and val2 == 6:
            win = True
        if data.bet == "double" and val1 == val2:
            win = True
        if data.bet == "sum_even" and total % 2 == 0:
            win = True
        if data.bet == "sum_odd" and total % 2 != 0:
            win = True
    elif data.game_mode == "multiply":
        result_text += f"Произведение: {product}\n"
        if data.bet == "1_18" and 1 <= product < 18:
            win = True
        if data.bet == "18_36" and 18 <= product <= 36:
            win = True
    elif data.game_mode == "plus_minus_7":
        result_text += f"Сумма: {total}\n"
        if data.bet == "more_7" and total > 7:
            win = True
        if data.bet == "equal_7" and total == 7:
            win = True
        if data.bet == "less_7" and total < 7:
            win = True

    result_text += "\n🎉 Вы победили!" if win else "\n😔 Вы проиграли."
    await message.answer(result_text, reply_markup=get_main_menu_keyboard())
