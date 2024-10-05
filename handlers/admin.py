from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
import re
from database import database
from setting import settings


class Form(StatesGroup):
    login = State()
    general = State()
    cmd_add_link = State()


admin_router = Router()


@admin_router.message(Command('admin'))
async def cmd_admin(message: Message, state: FSMContext):
    admin = database.find_user(message.from_user.id)
    if not admin:
        await message.answer('Вы ещё не проходили регистрацию (/start)')
        return
    if not admin.status:
        await message.answer('Введите пароль')
        await state.set_state(Form.login)
        return
    await message.answer("Слушаю")
    await state.set_state(Form.general)
    # database.create_user(message.from_user.username, message.from_user.id)
    # await message.answer('Вы зарегистрированы')


@admin_router.message(StateFilter(Form.login))
async def cmd_login(message: Message, state: FSMContext):
    if message.text == settings['SUPER_PASSWORD']:
        await message.answer('Удачно, слушаю')
        database.admin_update(message.from_user.id)
        await state.set_state(Form.general)
    else:
        await message.answer('НЕ Удачно')
    await state.clear()

@admin_router.message(StateFilter(Form.general))
async def cmd_general(message: Message, state: FSMContext):
    await message.answer(str(database.list_users()))
    await state.clear()
    await message.answer(str(database.command(message.text, 1)))

@admin_router.message(Command('addlink'))
async def cmd_add_link(message: Message, state: FSMContext):
    if database.find_user(message.from_user.id).status:
        await message.answer(str(database.list_users()))
        await state.set_state(Form.cmd_add_link)


@admin_router.message(Form.cmd_add_link)
async def cmd_add_link2(message: Message, state: FSMContext):
    if re.match("vless://", message.text):
        with open("links.txt", "a", encoding="utf-8") as f:
            f.write(message.text + "\n")
        f.close()
        await message.answer("Удачно")
    else:
        await message.answer("Не удачно")
    await state.clear()

