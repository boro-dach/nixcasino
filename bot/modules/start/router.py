from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.filters import Command

router = Router()

inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎰 Играть", callback_data="inline:play"),
            InlineKeyboardButton(text="👤 Профиль", callback_data="inline:profile"),
            InlineKeyboardButton(text="🎁 Бонус", callback_data="inline:bonus"),
        ],
        [
            InlineKeyboardButton(text="👥 Рефка", callback_data="inline:ref"),
            InlineKeyboardButton(text="🎫 Чеки", callback_data="inline:checks"),
            InlineKeyboardButton(text="🏆 Топ", callback_data="inline:top"),
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


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    name = user.full_name if user else "Игрок"
    greeting_text = f"🔥 Добро пожаловать, {name}!"
    await message.answer(greeting_text)

    await message.answer(
        "🚀 Канал где публикуются ставки, акции, новости - https://t.me/ColdSpin",
        reply_markup=inline_menu,
    )
