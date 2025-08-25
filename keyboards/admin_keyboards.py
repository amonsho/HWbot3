from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_add = KeyboardButton(text='➕ Добавить книгу')
button_delete = KeyboardButton(text='❌ Удалить книгу')
buttom_watch = KeyboardButton(text='👀 Смотреть отзывы пользователей')

admin_keyboard = ReplyKeyboardMarkup(keyboard=[[button_add],[button_delete,buttom_watch]],resize_keyboard=True)