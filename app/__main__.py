from aiogram import Dispatcher
from aiogram.utils import executor

from app import utils, config
from app.loader import dp
from config import conf
# The configuration of the modules using import
from app import middlewares, filters, handlers


async def on_startup(dispatcher: Dispatcher):
    await utils.setup_default_commands(dispatcher)
    await utils.notify_admins("Bot started", conf.tg_bot.admin_ids)


async def on_sthutdown(dispatcher: Dispatcher):
    await utils.notify_admins("Bot shutdown", conf.tg_bot.admin_ids)

if __name__ == '__main__':
    utils.setup_logger("INFO", ["sqlalchemy.engine", "aiogram.bot.api"])
    # utils.setup_logger("DEBUG")
    executor.start_polling(
        dp, on_startup=on_startup, on_shutdown=on_sthutdown, skip_updates=config.SKIP_UPDATES
    )
