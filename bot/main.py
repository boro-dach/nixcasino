import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

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
from services.api_client import api_client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.include_router(start_router)      
    dp.include_router(menu_router)       
    dp.include_router(games_router)      
    
    dp.include_router(dice_router)
    dp.include_router(bowling_router)
    dp.include_router(basketball_router)
    dp.include_router(darts_router)
    dp.include_router(football_router)
    dp.include_router(custom_games_router)
    
    dp.include_router(profile_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info("✅ Бот запущен и готов к работе!")
    logger.info(f"🔗 Backend URL: {settings.BACKEND_URL}")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        await bot.session.close()
        await api_client.close()
        logger.info("🛑 Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("❌ Бот остановлен пользователем")