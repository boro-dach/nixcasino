import httpx
from config import BACKEND_URL


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def get_or_create_user(self, telegram_id: int, username: str | None) -> dict:
        payload = {
            "telegramId": telegram_id,
            "username": username if username else "unknown",
        }
        try:
            response = await self.client.post("/user", json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    async def get_user_profile(self, telegram_id: int) -> dict:
        try:
            response = await self.client.get(f"/user/{telegram_id}")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Ошибка при запросе профиля: {e}")
            return None

    async def close(self):
        await self.client.aclose()


api_client = APIClient(base_url=BACKEND_URL)
