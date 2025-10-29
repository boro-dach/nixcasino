import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards import get_bowling_keyboard
from .callback_data import BowlingCallbackData

router = Router()


@router.callback_query(F.data == "bowling")
async def start_bowling(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎳 Боулинг\n\nСможете выбить страйк?", reply_markup=get_bowling_keyboard()
    )
    await callback.answer()


@router.callback_query(BowlingCallbackData.filter())
async def handle_bowling_bet(
    callback: CallbackQuery, callback_data: BowlingCallbackData
):
    await callback.message.edit_text("Катим шар...")
    await callback.answer()

    dice_msg = await callback.message.answer_dice(emoji="🎳")
    await asyncio.sleep(4)

    # Логика определения результата на основе значения кубика `🎳`
    # 1 = мимо
    # 2, 3, 4, 5 = сбито несколько кеглей (не страйк и не мимо)
    # 6 = страйк
    value = dice_msg.dice.value
    outcome = ""
    win = False

    if value == 1:
        outcome = "miss"
    elif value == 6:
        outcome = "strike"
    else:
        outcome = "hit"

    if callback_data.bet == outcome:
        win = True

    outcome_text_map = {
        "miss": "Шар прокатился мимо!",
        "strike": "СТРАЙК! Все кегли сбиты!",
        "hit": f"Неплохо, сбито {value - 1} кеглей, но это не страйк.",
    }

    result_text = f"🎳 {outcome_text_map.get(outcome)}\n\n"
    result_text += "🎉 Вы победили!" if win else "😔 Вы проиграли."

    await callback.message.answer(result_text, reply_markup=get_bowling_keyboard())
