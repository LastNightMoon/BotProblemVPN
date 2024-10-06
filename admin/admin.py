from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
import re
from database import database
from setting import settings


# Состояния для администратора
class Form(StatesGroup):
    login = State()
    general = State()
    cmd_add_link = State()


admin_router = Router()

# Команда /admin — вход в режим администратора
@admin_router.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    admin = database.find_user(message.from_user.id)
    if not admin:
        await message.answer('⚠️ Вы ещё не проходили регистрацию. Пожалуйста, используйте команду /start.')
        return
    if not admin.status:
        await message.answer('🔐 Введите пароль для подтверждения прав администратора.')
        await state.set_state(Form.login)
        return
    await message.answer("🔧 Добро пожаловать в режим администратора. Слушаю ваши команды.")
    await state.set_state(Form.general)


# Проверка пароля администратора
@admin_router.message(StateFilter(Form.login))
async def cmd_login(message: Message, state: FSMContext):
    if message.text == settings['SUPER_PASSWORD']:
        await message.answer('✅ Пароль успешно подтверждён. Теперь вы можете управлять ботом.')
        database.admin_update(message.from_user.id)
        await state.set_state(Form.general)
    else:
        await message.answer('❌ Неправильный пароль. Попробуйте ещё раз.')
    await state.clear()


# Основное состояние администратора для ввода команд
@admin_router.message(StateFilter(Form.general))
async def cmd_general(message: Message, state: FSMContext):
    await message.answer("📋 Список зарегистрированных пользователей:")
    await message.answer(str(database.list_users()))
    await message.answer("Введите SQL-запрос или используйте команды для управления.")
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


# Команда /help — помощь для администраторов
@admin_router.message(Command('help'))
async def cmd_admin_help(message: Message):
    help_text = (
        "ℹ️ <b>Помощь для администратора:</b>\n"
        "1. <b>/admin</b> — Вход в режим администратора (введите пароль).\n"
        "2. <b>/addlink</b> — Добавить новую ссылку формата vless://.\n"
        "3. <b>/help</b> — Показать это сообщение помощи.\n\n"
        "🚫 <i>Будьте осторожны с командами и SQL-запросами, они могут повлиять на работу бота и базы данных.</i>"
    )
    await message.answer(help_text)

