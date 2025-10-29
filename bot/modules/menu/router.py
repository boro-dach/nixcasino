from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

router = Router()

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎮 Играть", callback_data="play"),
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        ],
        [
            InlineKeyboardButton(text="🎰 Бонус спин", callback_data="bonus"),
            InlineKeyboardButton(text="💸 Реф. программа", callback_data="ref"),
        ],
        [
            InlineKeyboardButton(text="🎫 Чеки", callback_data="checks"),
            InlineKeyboardButton(text="🏆 Топ игроков", callback_data="top"),
        ],
    ]
)

reply_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Кошелёк"),
            KeyboardButton(text="Играть"),
            KeyboardButton(text="Меню"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)


@router.message(F.text == "Меню")
async def show_menu(message: Message):
    await message.answer(
        "🚀 Канал где публикуются ставки, акции, новости - https://t.me/ColdSpin",
        reply_markup=inline_menu,
    )
