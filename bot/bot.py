import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN_BOT
from handlers import router as user_router
from handlers_admin import router as admin_router
from db_utils import ensure_db_ready
from aiogram.fsm.storage.memory import MemoryStorage

async def main():
    bot = Bot(token=TOKEN_BOT)
    dp = Dispatcher(storage=MemoryStorage())

    await ensure_db_ready()

    dp.include_router(user_router)
    dp.include_router(admin_router)

    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
