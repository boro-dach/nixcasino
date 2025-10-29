import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards import get_custom_game_keyboard
from .callback_data import CustomGameCallbackData

router = Router()


@router.callback_query(F.data == "play_custom")
async def start_custom_game(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎰 Авторские игры\n\n"
        "Слот-машина выдаст число от 1 до 64.\n"
        "Ваша задача — угадать, в какой диапазон оно попадет. "
        "Чем меньше диапазон, тем выше выигрыш!",
        reply_markup=get_custom_game_keyboard(),
    )
    await callback.answer()


@router.callback_query(CustomGameCallbackData.filter())
async def handle_custom_game_bet(
    callback: CallbackQuery, callback_data: CustomGameCallbackData
):
    await callback.message.edit_text("Запускаем слот-машину...")
    await callback.answer()

    # Эмодзи "🎰" возвращает число от 1 до 64
    dice_msg = await callback.message.answer_dice(emoji="🎰")
    await asyncio.sleep(3)

    value = dice_msg.dice.value
    user_bet = callback_data.bet
    win = False

    if user_bet == "1_20" and 1 <= value <= 20:
        win = True
    elif user_bet == "21_40" and 21 <= value <= 40:
        win = True
    elif user_bet == "41_60" and 41 <= value <= 60:
        win = True
    elif user_bet == "jackpot" and 61 <= value <= 64:
        win = True

    result_text = f"🎰 Выпало число: {value}\n\n"
    result_text += "🎉 Вы победили!" if win else "😔 Вы проиграли."

    await callback.message.answer(result_text, reply_markup=get_custom_game_keyboard())
