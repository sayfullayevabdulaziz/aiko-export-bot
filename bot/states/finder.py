from aiogram.fsm.state import State, StatesGroup


class FinderState(StatesGroup):
    find = State()