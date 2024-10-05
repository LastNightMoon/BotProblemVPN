import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.admin import admin_router
from handlers.usually_user import user_router
from scheduler_g import check_date_payment, check_payment
from setting import settings
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

async def main():
    dp.include_router(admin_router)
    dp.include_router(user_router)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # Добавление задачи для выполнения каждый день в 19:00
    scheduler.add_job(check_date_payment, CronTrigger(hour=19, minute=0), args=(bot,))
    # scheduler.add_job(check_date_payment, IntervalTrigger(seconds=50), args=(bot, ))
    # await check_date_payment(bot)
    # Запуск планировщика
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if '__main__' == __name__:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    bot = Bot(token=settings['TOKEN_BOT'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    asyncio.run(main())
