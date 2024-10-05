from datetime import datetime, timedelta, date

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import State

from database import database
from yoomoney_work import get_link_for_payment

user_router = Router()
err = State()

@user_router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    if database.find_user(message.from_user.id):
        await message.answer('Вы уже проходили регистрацию')
        return
    # Открываем файл для чтения и записи
    with open("links.txt", "r+", encoding="utf-8") as file:
        lines = file.readlines()
        date_first_payment = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        if lines:
            first_line = lines.pop(0).strip()  # Удаляем первую строку и убираем лишние символы новой строки
            # print(f"Первая строка: {first_line}")  # Выводим первую строку на экран
            file.seek(0)
            file.truncate(0)
            file.writelines(lines)
            await message.answer("Ваша ссылка для подключения к vpn")
            await message.answer(f"<pre><code>{first_line}</code></pre>")
            database.create_user(message.from_user.username, message.from_user.id, date_first_payment, link=first_line)
            await message.answer('Вы зарегистрированы')
        else:
            await message.answer("В настоящее время у нас закончились места, но в ближайшие несколько минут появятся, "
                                 "пожалуйста подождите и попробуйте снова")
            for admin in database.list_admin():
                await bot.send_message(admin, "Внимание в файле закончились ссылки")
        file.close()


@user_router.message(Command('error'))
async def cmd_get_error(message: Message, state: FSMContext):
    await message.answer('Расскажите что произошло')
    await state.set_state(err)

@user_router.message(F.text, err)
async def cmd_get_error(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Уведомление получено, проблему уже решают')
    await state.clear()
    for admin in database.list_admin():
        await bot.send_message(admin.chat_id, message.text)

@user_router.message(Command("payment"))
async def cmd_payment(message: Message, bot: Bot):
    user = database.find_user(message.from_user.id)
    if (date.today() - timedelta(days=8)).strftime('%Y-%m-%d') < user.date <= (
            date.today() + timedelta(days=1)).strftime('%Y-%m-%d'):
        await message.answer("Ссылка для оплаты")
        await message.answer(f"{get_link_for_payment(user)}")
    else:
        year, month, day = user.date.split("-")
        await message.answer(f"Ещё рано, ссылка придёт {(datetime(year, month, day) - timedelta(days=1)).strftime('%Y-%m-%d')}")