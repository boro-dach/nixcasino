import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from modules.start.router import router as start_router
from modules.dice.router import router as dice_router
from modules.menu.router import router as menu_router
from modules.games.router import router as games_router
from modules.bowling.router import router as bowling_router
from modules.basketball.router import router as basketball_router
from modules.darts.router import router as darts_router
from modules.football.router import router as football_router
from modules.custom_games.router import router as custom_games_router
from modules.profile.router import router as profile_router

from config import settings

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(games_router)
    dp.include_routers(
        dice_router,
        bowling_router,
        basketball_router,
        darts_router,
        football_router,
        custom_games_router,
    )
    dp.include_router(profile_router)

    print("✅ Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
