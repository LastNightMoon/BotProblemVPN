# Состояния для администратора
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.filters import BaseFilter

from database import database


class Form(StatesGroup):
    login = State()
    general = State()
    cmd_add_link = State()

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = database.find_user(message.from_user.id)
        return user is not None and user.status