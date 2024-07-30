from aiogram.fsm.state import State, StatesGroup


class RegisterFormState(StatesGroup):
    number = State()