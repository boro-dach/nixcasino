from aiogram.filters.callback_data import CallbackData


class CustomGameCallbackData(CallbackData, prefix="cg"):
    bet: str
