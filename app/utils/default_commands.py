from aiogram import types
from loguru import logger
from app.config import commands


async def setup_default_commands(dp):
    await dp.bot.set_my_commands(
        [types.BotCommand(name, description) for name, description in commands]
    )

logger.info('Standard commands are successfully configured')
