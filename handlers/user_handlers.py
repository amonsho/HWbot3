from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.user_keyboards import user_keyboard
from keyboards.admin_keyboards import admin_keyboard

from database.users import User
from database.books import Book
from database.reviews import Review

from states.state import ReviewState

from database.db import db

user_router = Router()

b1=Book(db)


@user_router.message(Command('start'))
async def start_handler(msg:Message):
    u1 = User(msg.from_user.id,msg.from_user.full_name, db)
    user = await u1.get_user()
    if not user:
        await u1.add_user()
    
    if await u1.check_status():
        await msg.answer('Добро пожаловать, админ!',reply_markup=admin_keyboard)
    else:
        await msg.answer('Добро пожаловать в книжный клуб!',reply_markup=user_keyboard)

@user_router.message(lambda m: m.text == '📚 Список книг')
async def list_books(msg:Message):
    books = await b1.get_books()
    if not books:
        await msg.answer('Книг пока нет.')
        return
    

    for b in books:
        text = "\n".join([f"{b['id']}. {b['title']} — {b['author']} ({b['year']})"])
        await msg.answer("📚 Список книг:\n\n" + text)


@user_router.message(lambda m: m.text == "➕ Добавить отзыв")
async def add_review_start(msg: Message, state: FSMContext):
    books = await b1.get_books()
    if not books:
        await msg.answer("❌ Книг пока нет.")
        return

    for b in books:
        text = "\n".join([f"{b['id']}. {b['title']}"])
        await msg.answer("📖 Выберите книгу по ID:\n\n" + text)
        await state.set_state(ReviewState.choose_book)

@user_router.message(ReviewState.choose_book)
async def otziv_book_id(msg:Message, state:FSMContext):
    await state.update_data(book_id=int(msg.text))
    await msg.answer('Введите ваш отзыв: ')
    await state.set_state(ReviewState.enter_text)


@user_router.message(ReviewState.enter_text)
async def save_review(msg: Message, state: FSMContext):
    data = await state.get_data()
    book_id = data["book_id"]

    user = User(msg.from_user.id, msg.from_user.full_name, db)
    user_row = await user.get_user_row()

    r1=Review(db)
    await r1.add_review(user_id=user_row["id"], book_id=book_id, review_text=msg.text)

    await msg.answer("Отзыв сохранён!")
    await state.clear()

@user_router.message(lambda m: m.text == "📝 Мои отзывы")
async def my_reviews(msg: Message):

    user = User(msg.from_user.id, msg.from_user.full_name, db)
    user_row = await user.get_user_row() 

    if not user_row:
        await msg.answer(" Пользователь не найден.")
        return


    reviews = await Review.get_user_review(user_id=user_row["id"])
    if not reviews:
        await msg.answer("❌ У вас нет отзывов.")
        return
    
    for r in reviews:
        text = "\n\n".join([f"{r['title']}\n {r['review_text']}"])
        await msg.answer("📝 Ваши отзывы:\n\n" + text)









    


