from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from .keyboards import get_games_menu

router = Router()


@router.message(F.text == "Играть")
async def games_menu(message: Message):
    await message.answer(
        "🎮 Выберите игру, на которую хотите сделать ставку!\n\n"
        "🔒 Итог каждой игры приходит с серверов Telegram – это "
        "гарантирует прозрачность и честность! Резерв бота /reserve.",
        reply_markup=get_games_menu(),
    )


@router.callback_query(F.data == "play")
async def play_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎮 Выберите игру, на которую хотите сделать ставку!\n\n"
        "🔒 Итог каждой игры приходит с серверов Telegram – это "
        "гарантирует прозрачность и честность! Резерв бота /reserve.",
        reply_markup=get_games_menu(),
    )
    await callback.answer()
