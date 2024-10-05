from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters.state import State

from database import database

start_router = Router()
err = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    if database.find_user(message.from_user.id):
        await message.answer('Вы уже проходили регистрацию')
        return
    # Открываем файл для чтения и записи
    with open("links.txt", "r+", encoding="utf-8") as file:
        # Считываем все строки в список
        lines = file.readlines()
        if lines:
            # Извлекаем первую строку и удаляем её из списка
            first_line = lines.pop(0).strip()  # Удаляем первую строку и убираем лишние символы новой строки
            print(f"Первая строка: {first_line}")  # Выводим первую строку на экран

            # Перемещаем курсор в начало файла и очищаем его содержимое
            file.seek(0)
            file.truncate(0)

            # Записываем оставшиеся строки обратно в файл
            file.writelines(lines)
            await message.answer("Ваша ссылка для подключения к vpn")
            await message.answer("```" + first_line + "```")

        else:
            await message.answer("В настоящее время у нас закончились места, но в ближайшие несколько минут появятся, "
                                 "пожалуйста подождите")
            for admin in database.list_admin():
                await bot.send_message(admin, "Внимание в файле закончились ссылки")
        file.close()
    await message.answer('Вы зарегистрированы')


@start_router.message(Command('error'))
async def cmd_get_error(message: Message, state: FSMContext):
    await message.answer('Расскажите что произошло')
    await state.set_state(err)

@start_router.message(F.text, err)
async def cmd_get_error(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Уведомление получено, проблему уже решают')
    await state.clear()

    for admin in database.list_admin():
        await bot.send_message(admin.chat_id, message.text)



