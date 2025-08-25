from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.state import AddBookState
from keyboards.admin_keyboards import admin_keyboard
from database.books import Book
from database.reviews import Review
from database.db import db

admin_router = Router()

@admin_router.message(lambda m: m.text == '➕ Добавить книгу')
async def add_book_start(msg:Message, state:FSMContext):
    await msg.answer('Введите название книги: ')
    await state.set_state(AddBookState.enter_title)

@admin_router.message(AddBookState.enter_title)
async def add_book_title(msg:Message, state:FSMContext):
    await state.update_data(title=msg.text)
    await msg.answer('Введите автора книги: ')
    await state.set_state(AddBookState.enter_author)

@admin_router.message(AddBookState.enter_author)
async def add_book_author(msg:Message, state:FSMContext):
    await state.update_data(author=msg.text)
    await msg.answer('Введите год выпуска книги: ')
    await state.set_state(AddBookState.enter_year)

@admin_router.message(AddBookState.enter_year)
async def add_book_year(msg:Message, state:FSMContext):
    data = await state.get_data()
    book = Book(db)
    await book.add_books(title=data['title'], author=data['author'], year=int(msg.text))
    await msg.answer('Книга добавлена!',reply_markup=admin_keyboard)
    await state.clear()

@admin_router.message(lambda m: m.text == "❌ Удалить книгу")
async def delete_book(msg: Message):
    book = Book(db) 
    books = await book.get_books()
    if not books:
        await msg.answer("Книг пока нет")
        return

    for b in books:
        text = "\n".join([f"{b['id']}. {b['title']}"])
        await msg.answer("Введите ID книги для удаления:\n\n" + text)

@admin_router.message(lambda m: m.text.isdigit())
async def confirm_delete_book(msg: Message):
    book = Book(db) 
    await book.delete_books(int(msg.text))
    await msg.answer("Книга удалена!")


@admin_router.message(lambda m: m.text == "👀 Смотреть отзывы пользователей")
async def view_reviews(msg: Message):
    r1 = Review(db)
    reviews = await r1.get_all_reviews()
    if not reviews:
        await msg.answer("Отзывов пока нет.")
        return
    
    for r in reviews:
        text = "\n\n".join(
            [f"👤 {r['fullname']} | 📖 {r['title']}\n✍️ {r['review_text']}"]
        )
        await msg.answer("👀 Отзывы пользователей:\n\n" + text)

