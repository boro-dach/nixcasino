import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from modules.start.router import router as start_router
from config import settings

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()

    dp.include_router(start_router)

    print("✅ Бот запущен")
    await dp.start_polling(bot)

    dp.include_router()


if __name__ == "__main__":
    asyncio.run(main())
