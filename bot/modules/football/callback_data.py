from aiogram.filters.callback_data import CallbackData


class FootballCallbackData(CallbackData, prefix="fb"):
    bet: str
