from aiogram.filters.callback_data import CallbackData


class BowlingCallbackData(CallbackData, prefix="bw"):
    bet: str
