from aiogram.filters.callback_data import CallbackData


class BasketballCallbackData(CallbackData, prefix="bb"):
    bet: str
