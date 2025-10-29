from aiogram.fsm.state import StatesGroup, State


class BetStates(StatesGroup):
    waiting_for_bet = State()
