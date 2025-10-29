import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards import get_basketball_keyboard
from .callback_data import BasketballCallbackData

router = Router()


@router.callback_query(F.data == "basketball")
async def start_basketball(callback: CallbackQuery):
    await callback.message.edit_text(
        "🏀 Баскетбол\n\nУгадайте исход броска.", reply_markup=get_basketball_keyboard()
    )


@router.callback_query(BasketballCallbackData.filter())
async def handle_basketball_bet(
    callback: CallbackQuery, callback_data: BasketballCallbackData
):
    await callback.message.edit_text("Бросаем мяч...")

    dice_msg = await callback.message.answer_dice(emoji="🏀")
    await asyncio.sleep(4)

    value = dice_msg.dice.value
    outcome = ""
    win = False

    if value <= 2:
        outcome = "miss"
    elif value == 3:
        outcome = "stuck"
    elif value == 4:
        outcome = "any_goal"
    elif value == 5:
        outcome = "clean_goal"

    if callback_data.bet == outcome:
        win = True
    elif callback_data.bet == "any_goal" and outcome == "clean_goal":
        win = True

    outcome_text_map = {
        "miss": "Промах!",
        "stuck": "Мяч застрял!",
        "any_goal": "Гол!",
        "clean_goal": "Чистый гол!",
    }

    result_text = f"🏀 {outcome_text_map[outcome]}\n\n"
    result_text += "🎉 Вы победили!" if win else "😔 Вы проиграли."

    await callback.message.answer(result_text, reply_markup=get_basketball_keyboard())
