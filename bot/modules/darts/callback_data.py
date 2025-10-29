from aiogram.filters.callback_data import CallbackData


class DartsCallbackData(CallbackData, prefix="darts"):
    bet: str
