from aiogram import Dispatcher
from aiogram.utils import executor

from app import utils
from app.loader import dp
from app.config import conf
# The configuration of the modules using import
from app import middlewares, filters, handlers


async def on_startup(dispatcher: Dispatcher):
    await utils.setup_default_commands(dispatcher)
    await utils.notify_admins("Bot started", conf.tg_bot.admin_ids)
    return True


async def on_sthutdown(dispatcher: Dispatcher):
    # db.close()
    await utils.notify_admins("Bot shutdown", conf.tg_bot.admin_ids)
    return True


if __name__ == '__main__':
    # utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api", "aiogram.contrib.middlewares.logging"])
    # utils.setup_logger("DEBUG", ["sqlalchemy.engine", "aiogram.bot.api"])
    # utils.setup_logger("INFO", ["aiogram.bot.api"])
    utils.setup_logger("DEBUG", [])

    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_sthutdown, skip_updates=conf.tg_bot.skip_updates
    )
