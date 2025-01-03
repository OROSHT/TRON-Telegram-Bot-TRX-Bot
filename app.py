print("Modules")
import logging
import asyncio
from utils.db_api.db_file import db
from loader import dp, db
from utils.set_bot_commands import set_default_commands
from middleware.middleware import UserBanned
import data.config as config
from utils.misc.Trx import get_course
from aiogram import executor

async def update_course_pool():
    while True:
        try:
            course = await get_course()
            await db.update_course(course)
        except Exception as e:
            logging.error(f"Failed to update course: {e}")
        await asyncio.sleep(config.rate * 60)

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    dp.middleware.setup(UserBanned())
    await db.check_start()
    asyncio.create_task(update_course_pool())

if __name__ == '__main__':
    print("main")
    try:
        executor.start_polling(dp, on_startup=on_startup)
    except Exception as err:
        logging.exception(err)
        