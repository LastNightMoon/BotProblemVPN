import datetime
from calendar import month

from aiogram import Bot
from yoomoney import Authorize, Client, Quickpay

from database import database
from setting import settings
from yoomoney_work import get_link_for_payment


async def check_date_payment(bot: Bot):
    admins = database.list_admin()
    client = Client(settings['TOKEN_YOOMONEY'])
    history = client.operation_history(from_date=(datetime.datetime.today() - datetime.timedelta(days=1)))
    for operation in history.operations:
        user = database.find_user(operation.label)
        if not user:
            continue
        date = datetime.date(*map(int, user.date.split("-")))
        new_date = datetime.timedelta(days=30) + date
        # Обновление значения даты в базе данных
        database.update_date_from_id(user.chat_id, new_date.strftime('%Y-%m-%d'))
    for user in database.list_users():
        if user.date == (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'):
            await bot.send_message(user.chat_id, f"Здравствуйте, нужно оплатить")
            await bot.send_message(user.chat_id, f"{get_link_for_payment(user)}")
        elif (datetime.date.today() - datetime.timedelta(days=8)).strftime('%Y-%m-%d') < user.date < (
                datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'):

            await bot.send_message(user.chat_id, "Отключаем вас, оплатите в течении недели вот ссылка")
            await bot.send_message(user.chat_id, f"{get_link_for_payment(user)}")
            for admin in admins:
                await bot.send_message(admin.chat_id, str(user) + "Вырубай его")
        elif (datetime.date.today() - datetime.timedelta(days=8)).strftime('%Y-%m-%d') == user.date:
            await bot.send_message(user.chat_id, "Удаляем вас, за неправомерное использование возможен запрет на использование будте аккуратны")
            for admin in admins:
                await bot.send_message(admin.chat_id, str(user) + "удали его")


def check_payment(bot: Bot):
    pass
