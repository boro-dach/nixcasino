from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_games_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎲", callback_data="dice"),
                InlineKeyboardButton(text="⚽", callback_data="football"),
                InlineKeyboardButton(text="🏀", callback_data="basketball"),
                InlineKeyboardButton(text="🎯", callback_data="darts"),
                InlineKeyboardButton(text="🎳", callback_data="bowling"),
            ],
            [
                InlineKeyboardButton(
                    text="🎰 Telegram игры", callback_data="menu:telegram_games"
                ),
                InlineKeyboardButton(text="🎲 Авторские", callback_data="play_custom"),
            ],
            [
                InlineKeyboardButton(
                    text="🎲 Раздачи", url="https://t.me/your_channel"
                ),
                InlineKeyboardButton(
                    text="🎮 Игровой чат", url="https://t.me/your_chat"
                ),
            ],
        ]
    )
    return keyboard


def get_telegram_games_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎰 Слоты", callback_data="tg_game:slots"),
                InlineKeyboardButton(text="🎲 Кости", callback_data="tg_game:dice"),
            ],
            [
                InlineKeyboardButton(text="🎯 Дартс", callback_data="tg_game:darts"),
                InlineKeyboardButton(
                    text="🏀 Баскетбол", callback_data="tg_game:basketball"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚽ Футбол", callback_data="tg_game:football"
                ),
                InlineKeyboardButton(
                    text="🎳 Боулинг", callback_data="tg_game:bowling"
                ),
            ],
            [
                InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main"),
            ],
        ]
    )
    return keyboard


def get_custom_games_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🃏 Блэкджек", callback_data="custom_game:blackjack"
                ),
                InlineKeyboardButton(
                    text="🎰 Рулетка", callback_data="custom_game:roulette"
                ),
            ],
            [
                InlineKeyboardButton(text="🎲 Краш", callback_data="custom_game:crash"),
                InlineKeyboardButton(text="💣 Мины", callback_data="custom_game:mines"),
            ],
            [
                InlineKeyboardButton(text="◀️ Назад", callback_data="menu:main"),
            ],
        ]
    )
    return keyboard


def get_reply_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💰 Кошелёк"),
                KeyboardButton(text="🎰 Играть"),
                KeyboardButton(text="📋 Меню"),
            ]
        ],
        resize_keyboard=True,
    )
