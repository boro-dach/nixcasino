from aiogram.filters.callback_data import CallbackData


class ProfileCallbackData(CallbackData, prefix="prof"):
    action: str
