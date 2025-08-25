import asyncio

from aiogram import Dispatcher, Bot

from database.db import db

from handlers.user_handlers import user_router

from handlers.admin_handlers import admin_router


bot = Bot('8330771740:AAHZOkc80ObqdhiXC1fc1HLPJXCgjyFCTco')

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)

async def main():
    await db.connect()
    await db.create_tables()
    await dp.start_polling(bot)
    await db.close()

if __name__ == '__main__':
    asyncio.run(main())