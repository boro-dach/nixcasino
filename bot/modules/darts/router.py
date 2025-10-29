import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards import get_darts_keyboard
from .callback_data import DartsCallbackData

router = Router()


@router.callback_query(F.data == "darts")
async def start_darts(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎯 Дартс\n\nУгадайте, куда попадет дротик?", reply_markup=get_darts_keyboard()
    )


@router.callback_query(DartsCallbackData.filter())
async def handle_darts_bet(callback: CallbackQuery, callback_data: DartsCallbackData):
    await callback.message.edit_text("Бросаем дротик...")

    dice_msg = await callback.message.answer_dice(emoji="🎯")
    await asyncio.sleep(4)

    # Логика определения результата на основе значения кубика `🎯`
    # 1 = промах
    # 2, 3, 4, 5 = попадание в сектор
    # 6 = в яблочко (центр)
    value = dice_msg.dice.value
    outcome = ""
    win = False

    if value == 1:
        outcome = "miss"
    # Произвольно делим сектора на "красные" и "белые"
    elif value in [2, 4]:
        outcome = "red"
    elif value in [3, 5]:
        outcome = "white"
    elif value == 6:
        outcome = "center"

    # Проверяем, совпадает ли результат со ставкой пользователя
    if callback_data.bet == outcome:
        win = True

    outcome_text_map = {
        "miss": "Промах!",
        "red": "Попадание в красный сектор!",
        "white": "Попадание в белый сектор!",
        "center": "Точно в яблочко!",
    }

    result_text = f"🎯 {outcome_text_map.get(outcome, 'Неизвестный результат')}\n\n"
    result_text += "🎉 Вы победили!" if win else "😔 Вы проиграли."

    await callback.message.answer(result_text, reply_markup=get_darts_keyboard())
