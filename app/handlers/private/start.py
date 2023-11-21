from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hcode

from app.loader import dp
from app.config import commands

# from app.middlewares import rate_limit

cb = CallbackData("post", "id", "action")


@dp.message_handler(CommandStart())
async def command_start_handler(msg: types.Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!\n Пройди регистрацию /reg\n Если не знаешь для чего она - 🖕')


# @rate_limit(5, "reg")
@dp.message_handler(commands="reg")
async def command_reg_handler(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id} \n\n Вы знаете кому его отправить")


# @rate_limit(5, "id")
@dp.message_handler(commands="id")
async def command_reg_handler(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id}")


# @rate_limit(5, "help")
@dp.message_handler(commands="help")
async def command_help_handler(message: types.Message):
    """Responds to /help with list of available commands, which're located in data/config.py"""

    # Generates a list
    answer = ["Available commands: "]
    for command, description in commands:
        answer.append(hcode(f"/{command}") + f" — {description}")

    await message.answer("\n".join(answer))
