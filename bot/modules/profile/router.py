from aiogram import Router, F
from aiogram.types import CallbackQuery
from datetime import datetime

from .keyboards import get_profile_keyboard, get_stats_keyboard
from .callback_data import ProfileCallbackData
from modules.menu.router import (
    inline_menu,
)

user_data = {}


def get_user(user_id: int):
    """Возвращает данные пользователя, создавая их при необходимости."""
    if user_id not in user_data:
        user_data[user_id] = {
            "balance": 100.0,
            "turnover": 0.0,
            "registration_date": datetime.now(),
            "games_played": 0,
            "total_deposits": 0.0,
            "total_withdrawals": 0.0,
            "is_private": False,
        }
        # Симулируем несколько игр для примера
        user_data[user_id]["turnover"] = 1250.50
        user_data[user_id]["games_played"] = 42
    return user_data[user_id]


router = Router()


async def show_profile(callback: CallbackQuery):
    """Отображает главный экран профиля. Вынесено в функцию для переиспользования."""
    user = get_user(callback.from_user.id)

    account_age = (datetime.now() - user["registration_date"]).days

    text = (
        f"👤 **Ваш профиль**\n\n"
        f"💰 **Баланс:** `{user['balance']}`\n"
        f"🔄 **Оборот ставок:** `{user['turnover']}`\n"
        f"🕹️ **Сыграно ставок:** `{user['games_played']}`\n"
        f"⏳ **Дней с нами:** `{account_age}`"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_profile_keyboard(user["is_private"]),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "profile")
async def handle_profile_entry(callback: CallbackQuery):
    await show_profile(callback)
    await callback.answer()


@router.callback_query(ProfileCallbackData.filter(F.action == "stats"))
async def handle_stats(callback: CallbackQuery):
    user = get_user(callback.from_user.id)
    account_age = (datetime.now() - user["registration_date"]).days
    username = (
        f"@{callback.from_user.username}" if callback.from_user.username else "Скрыт"
    )

    text = (
        f"📊 **Ваша статистика**\n\n"
        f"👤 **Пользователь:** `{username if not user['is_private'] else 'Скрыт'}`\n"
        f"🕹️ **Сыграно ставок:** `{user['games_played']}`\n"
        f"🔄 **Общий оборот:** `{user['turnover']}`\n"
        f"⏳ **Дней с нами:** `{account_age}`\n"
        f"📈 **Всего пополнено:** `{user['total_deposits']}`\n"
        f"📉 **Всего выведено:** `{user['total_withdrawals']}`"
    )

    await callback.message.edit_text(
        text, reply_markup=get_stats_keyboard(), parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(ProfileCallbackData.filter(F.action == "privacy_toggle"))
async def handle_privacy_toggle(callback: CallbackQuery):
    user = get_user(callback.from_user.id)
    user["is_private"] = not user["is_private"]

    status = "скрыт" if user["is_private"] else "виден"
    await callback.answer(f"Ваш никнейм теперь {status} для других", show_alert=True)

    await show_profile(callback)


@router.callback_query(F.data == "main_menu_from_profile")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🚀 Канал где публикуются ставки, акции, новости - https://t.me/ColdSpin",
        reply_markup=inline_menu(),
    )
    await callback.answer()


@router.callback_query(
    ProfileCallbackData.filter(
        F.action.in_({"deposit", "withdraw", "tx_history", "game_history"})
    )
)
async def handle_placeholders(callback: CallbackQuery):
    await callback.answer("Этот раздел находится в разработке.", show_alert=True)
