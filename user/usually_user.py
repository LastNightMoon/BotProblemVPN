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

# Команда /start
@user_router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    if database.find_user(message.from_user.id):
        await message.answer('⚠️ Вы уже проходили регистрацию.')
        return

    date_first_payment = (datetime.now() + timedelta(days=1))
    link = database.get_link()
    if link:
        await message.answer("🎉 Ваша ссылка для подключения к VPN:")
        await message.answer(f"<pre><code>{link}</code></pre>")
        database.create_user(message.from_user.username, message.from_user.id, date_first_payment, link=link)
        await message.answer('✅ Вы успешно зарегистрированы!')
        await cmd_help(message, bot)
    else:
        await message.answer("😕 В настоящее время все места заняты, но они скоро появятся. "
                             "Пожалуйста, подождите немного и попробуйте снова.")
        for admin in database.list_admin():
            await bot.send_message(admin, "⚠️ Внимание, в файле закончились ссылки.")

# Команда /help
@user_router.message(Command("help"))
async def cmd_help(message: Message, bot: Bot):
    help_text = (
        "ℹ️ <b>Помощь по боту:</b>\n"
        "1. <b>/start</b> — Регистрация и получение ссылки для VPN.\n"
        "2. <b>/payment</b> — Получить ссылку для оплаты (доступно за день до срока оплаты).\n"
        "3. <b>/error</b> — Сообщить о проблеме.\n"
        "4. <b>/help</b> — Показать это сообщение помощи.\n\n"
        "📌 Для дополнительных вопросов обращайтесь к администрации."
    )
    await message.answer(help_text)

# Команда /error
@user_router.message(Command('error'))
async def cmd_get_error(message: Message, state: FSMContext):
    await message.answer('⚠️ Пожалуйста, опишите проблему, и мы постараемся её решить.')
    await state.set_state(err)

# Команда /payment
@user_router.message(Command("payment"))
async def cmd_payment(message: Message, bot: Bot):
    user = database.find_user(message.from_user.id)
    if (date.today() - timedelta(days=8)) < user.date <= (
            date.today() + timedelta(days=1)):
        await message.answer("💳 Ссылка для оплаты:")
        await message.answer(f"{get_link_for_payment(user)}")
    else:
        payment_date = user.date - timedelta(days=1)
        await message.answer(f"⏳ Ещё рано для оплаты. Ссылка придёт {payment_date.strftime('%Y-%m-%d')}.")

# Обработка сообщений о проблеме
@user_router.message(err)
async def cmd_get_error(message: Message, state: FSMContext, bot: Bot):
    await message.answer('📩 Ваше сообщение получено. Мы уже работаем над решением проблемы!')
    await state.clear()
    for admin in database.list_admin():
        await bot.send_message(admin.chat_id,
                               f"🔔 Новое сообщение о проблеме от("
                               f"{database.find_user(message.from_user.id)}):\n\n{message.text}")