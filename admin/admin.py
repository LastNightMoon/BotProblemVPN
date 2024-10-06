from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
import re

from admin.midleware import AdminMiddleware
from database import database
from setting import settings
from utils import Form, IsAdminFilter

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    await message.answer("🔧 Добро пожаловать в режим администратора. Слушаю ваши команды.")
    await message.answer("📋 Список зарегистрированных пользователей:")
    await message.answer(str(database.list_users()))
    await state.set_state(Form.general)
    await message.answer("Введите SQL-запрос или используйте команды для управления.")


# Основное состояние администратора для ввода команд
@admin_router.message(StateFilter(Form.general))
async def cmd_general(message: Message, state: FSMContext):
    try:
        await message.answer(database.command(message.text))
    except Exception as e:
        print(e)
    await state.clear()


# Команда /addlink — добавление новой ссылки
@admin_router.message(Command('addlink'))
async def cmd_add_link(message: Message, state: FSMContext):
    user = database.find_user(message.from_user.id)
    if user and user.status:
        await message.answer('🔗 Пожалуйста, введите ссылку формата vless:// для добавления в базу.')
        await state.set_state(Form.cmd_add_link)
    else:
        await message.answer("❌ У вас нет прав для выполнения этой команды.")


# Обработка новой ссылки
@admin_router.message(Form.cmd_add_link)
async def cmd_add_link2(message: Message, state: FSMContext):
    if re.match(r"vless://", message.text):
        database.new_link(message.text)
        await message.answer("✅ Ссылка успешно добавлена!")
    else:
        await message.answer("❌ Неверный формат ссылки. Убедитесь, что она начинается с `vless://`.")
    await state.clear()


