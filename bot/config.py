from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Telegram Bot
    BOT_TOKEN: str
    
    # Backend API
    BACKEND_URL: str = "http://localhost:3000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()

# Экспорт для обратной совместимости
BOT_TOKEN = settings.BOT_TOKEN
BACKEND_URL = settings.BACKEND_URL