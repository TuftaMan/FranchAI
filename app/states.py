from aiogram.fsm.state import State, StatesGroup

class AskQuestion(StatesGroup):
    question = State()

