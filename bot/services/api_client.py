import httpx
from typing import Optional, Dict, Any
from config import BACKEND_URL
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    async def get_or_create_user(self, telegram_id: int, username: Optional[str]) -> Optional[Dict[str, Any]]:
        """Получить или создать пользователя"""
        payload = {
            "telegramId": telegram_id,
            "username": username if username else "unknown",
        }
        try:
            response = await self.client.post("/users", json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при создании пользователя: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка: {e.response.status_code}")
            return None

    async def get_user_profile(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получить профиль пользователя"""
        try:
            response = await self.client.get(f"/users/{telegram_id}")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при запросе профиля: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP ошибка: {e.response.status_code}")
            return None

    async def get_user_stats(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Получить статистику пользователя"""
        try:
            response = await self.client.get(f"/users/{telegram_id}/stats")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при запросе статистики: {e}")
            return None

    async def update_balance(self, telegram_id: int, amount: float) -> Optional[Dict[str, Any]]:
        """Обновить баланс пользователя"""
        try:
            response = await self.client.put(
                f"/users/{telegram_id}/balance",
                json={"amount": amount}
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при обновлении баланса: {e}")
            return None

    async def update_turnover(self, telegram_id: int, amount: float) -> Optional[Dict[str, Any]]:
        """Обновить оборот пользователя"""
        try:
            response = await self.client.put(
                f"/users/{telegram_id}/turnover",
                json={"amount": amount}
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при обновлении оборота: {e}")
            return None

    async def add_deposit(self, telegram_id: int, amount: float) -> Optional[Dict[str, Any]]:
        """Добавить депозит"""
        try:
            response = await self.client.put(
                f"/users/{telegram_id}/deposit",
                json={"amount": amount}
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при добавлении депозита: {e}")
            return None

    async def add_withdrawal(self, telegram_id: int, amount: float) -> Optional[Dict[str, Any]]:
        """Добавить вывод средств"""
        try:
            response = await self.client.put(
                f"/users/{telegram_id}/withdraw",
                json={"amount": amount}
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Ошибка при добавлении вывода: {e}")
            return None

    async def close(self):
        """Закрыть HTTP клиент"""
        await self.client.aclose()


# Singleton instance
api_client = APIClient(base_url=BACKEND_URL)