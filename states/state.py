from aiogram.fsm.state import StatesGroup, State

class ReviewState(StatesGroup):
    choose_book = State()
    enter_text = State()

class AddBookState(StatesGroup):
    enter_title = State()
    enter_author = State()
    enter_year = State()