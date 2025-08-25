from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_1 = KeyboardButton(text='📚 Список книг')
button_2 = KeyboardButton(text='➕ Добавить отзыв')
button_3 = KeyboardButton(text='📝 Мои отзывы')

user_keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2,button_3]],resize_keyboard=True)