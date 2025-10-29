from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callback_data import ProfileCallbackData


def get_profile_keyboard(is_private: bool):
    builder = InlineKeyboardBuilder()

    privacy_text = "✅ Показать ник" if is_private else "🙈 Скрыть ник"

    builder.button(
        text="💳 Пополнить", callback_data=ProfileCallbackData(action="deposit")
    )
    builder.button(
        text="💸 Вывести", callback_data=ProfileCallbackData(action="withdraw")
    )
    builder.button(
        text="📊 Статистика", callback_data=ProfileCallbackData(action="stats")
    )
    builder.button(
        text=privacy_text, callback_data=ProfileCallbackData(action="privacy_toggle")
    )
    builder.button(text="⬅️ Назад в меню", callback_data="main_menu_from_profile")
    builder.adjust(2)
    return builder.as_markup()


def get_stats_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="📜 История транзакций",
        callback_data=ProfileCallbackData(action="tx_history"),
    )
    builder.button(
        text="🎮 История игр", callback_data=ProfileCallbackData(action="game_history")
    )
    builder.button(text="⬅️ Назад в профиль", callback_data="profile")
    builder.adjust(1)
    return builder.as_markup()
