"""Вспомогательные функции для игр"""
from typing import Optional, Tuple
from api_client import api_client
import logging

logger = logging.getLogger(__name__)


async def process_game_bet(
    user_id: int,
    bet_amount: float
) -> Tuple[bool, Optional[dict], str]:
    """
    Обработать ставку игрока
    
    Returns:
        (success, user_data, error_message)
    """
    user = await api_client.get_user_profile(user_id)
    
    if not user:
        return False, None, "❌ Ошибка загрузки профиля"
    
    balance = user.get('balance', 0)
    
    if balance < bet_amount:
        return False, user, f"❌ Недостаточно средств!\nНужно: {bet_amount:.2f}\nУ вас: {balance:.2f}"
    
    # Снимаем ставку
    updated_user = await api_client.update_balance(user_id, -bet_amount)
    
    if not updated_user:
        return False, user, "❌ Ошибка при размещении ставки"
    
    return True, updated_user, ""


async def process_game_result(
    user_id: int,
    game_type: str,
    win: bool,
    bet_amount: float,
    win_amount: float
) -> Optional[dict]:
    """
    Обработать результат игры
    
    Args:
        user_id: ID пользователя
        game_type: Тип игры (DICE, DARTS, etc.)
        win: Выиграл ли игрок
        bet_amount: Сумма ставки
        win_amount: Сумма выигрыша
    
    Returns:
        Обновленные данные пользователя
    """
    # Начисляем выигрыш если есть
    if win and win_amount > 0:
        await api_client.update_balance(user_id, win_amount)
    
    # Сохраняем результат игры
    profit = win_amount - bet_amount
    await api_client.save_game_result(
        user_id,
        game_type,
        "WIN" if win else "LOSE",
        profit
    )
    
    # Возвращаем обновленные данные
    return await api_client.get_user_profile(user_id)


def format_game_result(
    win: bool,
    win_amount: float,
    balance: float,
    extra_info: str = ""
) -> str:
    """Форматировать текст результата игры"""
    result = f"{extra_info}\n" if extra_info else ""
    
    if win:
        result += f"🎉 **Выигрыш: {win_amount:.2f}**\n"
    else:
        result += "😔 **Проигрыш**\n"
    
    result += f"💰 Баланс: `{balance:.2f}`"
    
    return result