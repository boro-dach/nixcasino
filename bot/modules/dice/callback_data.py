# dice/callback_data.py
from aiogram.filters.callback_data import CallbackData


class DiceCallbackData(CallbackData, prefix="dice"):
    game_mode: str
    bet: str
