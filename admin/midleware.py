from aiogram import Router, BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from database import database


# Пример Middleware, которое проверяет права доступа администратора
class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = database.find_user(event.from_user.id)
        if user and user.status:
            return await handler(event, data)
        await event.answer("⛔ У вас нет прав для выполнения этой команды.")
        return None

