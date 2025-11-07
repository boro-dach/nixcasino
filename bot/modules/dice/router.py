import asyncio
import logging
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
from services.api_client import api_client

logger = logging.getLogger(__name__)
router = Router()

# Конфигурация ставок и коэффициентов
BET_AMOUNTS = {
    "single": 10.0,
    "double": 20.0,
    "multiply": 15.0,
    "plus_minus_7": 15.0,
    "specific_number": 50.0,
}

WIN_MULTIPLIERS = {
    "single": {"even": 2.0, "odd": 2.0, "more": 2.0, "less": 2.0},
    "double": {
        "both_even": 4.0,
        "both_odd": 4.0,
        "both_more": 4.0,
        "both_less": 4.0,
        "two_six": 30.0,
        "double": 6.0,
        "sum_even": 2.0,
        "sum_odd": 2.0,
    },
    "multiply": {"1_18": 2.0, "18_36": 2.0},
    "plus_minus_7": {"more_7": 2.0, "equal_7": 5.0, "less_7": 2.0},
    "specific_number": {str(i): 6.0 for i in range(1, 7)},
}


@router.callback_query(F.data == "dice")
async def show_dice_menu(callback: CallbackQuery):
    """Главное меню игры в кости"""
    user = await api_client.get_user_profile(callback.from_user.id)
    
    if not user:
        await callback.answer("❌ Ошибка загрузки профиля", show_alert=True)
        return
    
    await callback.message.edit_text(
        f"🎲 **Добро пожаловать в игру в кости!**\n\n"
        f"💰 Баланс: `{user.get('balance', 0):.2f}`\n\n"
        f"Выберите режим игры:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(DiceCallbackData.filter(F.bet == "menu"))
async def navigate_to_menu(callback: CallbackQuery, callback_data: DiceCallbackData):
    """Навигация по меню"""
    keyboards = {
        "main": (get_main_menu_keyboard, "Выберите режим:"),
        "single": (get_single_throw_keyboard, "🎲 Один бросок:\nСтавка: 10"),
        "double": (get_double_throw_keyboard, "🎲🎲 Два броска:\nСтавка: 20"),
        "multiply": (get_multiply_keyboard, "✖️ Произведение:\nСтавка: 15"),
        "plus_minus_7": (get_plus_minus_7_keyboard, "7️⃣ Сумма ±7:\nСтавка: 15"),
        "specific_number": (get_specific_number_keyboard, "🎯 На число:\nСтавка: 50"),
    }

    keyboard_func, text = keyboards.get(callback_data.game_mode, (get_main_menu_keyboard, "Выберите режим:"))
    await callback.message.edit_text(text, reply_markup=keyboard_func())
    await callback.answer()


@router.callback_query(DiceCallbackData.filter(F.bet != "menu"))
async def process_bet(callback: CallbackQuery, callback_data: DiceCallbackData):
    """Обработка ставки"""
    user_id = callback.from_user.id
    game_mode = callback_data.game_mode
    bet_amount = BET_AMOUNTS.get(game_mode, 10.0)
    
    # Проверка баланса
    user = await api_client.get_user_profile(user_id)
    if not user or user.get('balance', 0) < bet_amount:
        await callback.answer(
            f"❌ Недостаточно средств!\nНужно: {bet_amount:.2f}",
            show_alert=True
        )
        return
    
    # Снятие ставки
    if not await api_client.update_balance(user_id, -bet_amount):
        await callback.answer("❌ Ошибка размещения ставки", show_alert=True)
        return
    
    await callback.message.edit_text(f"💸 Ставка {bet_amount:.2f} принята!\n🎲 Бросаем кости...")
    await callback.answer()
    await asyncio.sleep(1)

    if game_mode in ["single", "specific_number"]:
        dice_msg = await callback.message.answer_dice(emoji="🎲")
        await asyncio.sleep(4)
        await _process_single_throw(callback.message, user_id, dice_msg.dice.value, callback_data, bet_amount)
    else:
        dice1_msg = await callback.message.answer_dice(emoji="🎲")
        await asyncio.sleep(4)
        dice2_msg = await callback.message.answer_dice(emoji="🎲")
        await asyncio.sleep(4)
        await _process_double_throw(callback.message, user_id, dice1_msg.dice.value, dice2_msg.dice.value, callback_data, bet_amount)


async def _process_single_throw(message: Message, user_id: int, value: int, data: DiceCallbackData, bet_amount: float):
    """Обработка одного броска"""
    win = False

    if data.game_mode == "single":
        win = (
            (data.bet == "even" and value % 2 == 0) or
            (data.bet == "odd" and value % 2 != 0) or
            (data.bet == "more" and value in {4, 5, 6}) or
            (data.bet == "less" and value in {1, 2, 3})
        )
    elif data.game_mode == "specific_number":
        win = int(data.bet) == value

    # Расчет выигрыша
    multiplier = WIN_MULTIPLIERS.get(data.game_mode, {}).get(data.bet, 0)
    win_amount = bet_amount * multiplier if win else 0
    profit = win_amount - bet_amount

    # Начисление выигрыша
    if win_amount > 0:
        await api_client.update_balance(user_id, win_amount)

    # Сохранение результата
    await api_client.save_game_result(
        user_id,
        "DICE",
        "WIN" if win else "LOSE",
        profit
    )

    # Получение нового баланса
    user = await api_client.get_user_profile(user_id)
    balance = user.get('balance', 0) if user else 0

    result_text = (
        f"🎲 **Выпало: {value}**\n\n"
        f"{'🎉 Выигрыш: ' + f'{win_amount:.2f}' if win else '😔 Проигрыш'}\n"
        f"💰 Баланс: `{balance:.2f}`"
    )

    await message.answer(result_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")


async def _process_double_throw(message: Message, user_id: int, val1: int, val2: int, data: DiceCallbackData, bet_amount: float):
    """Обработка двух бросков"""
    total = val1 + val2
    product = val1 * val2
    win = False

    if data.game_mode == "double":
        win = (
            (data.bet == "both_even" and val1 % 2 == 0 and val2 % 2 == 0) or
            (data.bet == "both_odd" and val1 % 2 != 0 and val2 % 2 != 0) or
            (data.bet == "both_more" and val1 > 3 and val2 > 3) or
            (data.bet == "both_less" and val1 < 4 and val2 < 4) or
            (data.bet == "two_six" and val1 == 6 and val2 == 6) or
            (data.bet == "double" and val1 == val2) or
            (data.bet == "sum_even" and total % 2 == 0) or
            (data.bet == "sum_odd" and total % 2 != 0)
        )
    elif data.game_mode == "multiply":
        win = (data.bet == "1_18" and 1 <= product < 18) or (data.bet == "18_36" and 18 <= product <= 36)
    elif data.game_mode == "plus_minus_7":
        win = (data.bet == "more_7" and total > 7) or (data.bet == "equal_7" and total == 7) or (data.bet == "less_7" and total < 7)

    # Расчет выигрыша
    multiplier = WIN_MULTIPLIERS.get(data.game_mode, {}).get(data.bet, 0)
    win_amount = bet_amount * multiplier if win else 0
    profit = win_amount - bet_amount

    # Начисление
    if win_amount > 0:
        await api_client.update_balance(user_id, win_amount)

    # Сохранение результата
    await api_client.save_game_result(user_id, "DICE", "WIN" if win else "LOSE", profit)

    # Новый баланс
    user = await api_client.get_user_profile(user_id)
    balance = user.get('balance', 0) if user else 0

    extra_info = ""
    if data.game_mode == "multiply":
        extra_info = f"Произведение: {product}\n"
    elif data.game_mode == "plus_minus_7":
        extra_info = f"Сумма: {total}\n"

    result_text = (
        f"🎲🎲 **Выпало: {val1} и {val2}**\n"
        f"{extra_info}\n"
        f"{'🎉 Выигрыш: ' + f'{win_amount:.2f}' if win else '😔 Проигрыш'}\n"
        f"💰 Баланс: `{balance:.2f}`"
    )

    await message.answer(result_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown")