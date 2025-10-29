import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards import get_football_keyboard
from .callback_data import FootballCallbackData

router = Router()


@router.callback_query(F.data == "football")
async def start_football(callback: CallbackQuery):
    await callback.message.edit_text(
        "⚽️ Футбол\n\nУгадайте, будет гол или промах?",
        reply_markup=get_football_keyboard(),
    )


@router.callback_query(FootballCallbackData.filter())
async def handle_football_bet(
    callback: CallbackQuery, callback_data: FootballCallbackData
):
    await callback.message.edit_text("Бьем по мячу...")

    dice_msg = await callback.message.answer_dice(emoji="⚽️")
    await asyncio.sleep(4)

    # Значения для ⚽️: 1=мимо, 2,3,4=рядом, 5=гол.
    is_goal = dice_msg.dice.value >= 5
    user_bet_is_goal = callback_data.bet == "goal"

    win = (is_goal and user_bet_is_goal) or (not is_goal and not user_bet_is_goal)

    result_text = f"⚽️ {'ГОЛ!' if is_goal else 'ПРОМАХ!'}\n\n"
    result_text += "🎉 Вы победили!" if win else "😔 Вы проиграли."

    await callback.message.answer(result_text, reply_markup=get_football_keyboard())
