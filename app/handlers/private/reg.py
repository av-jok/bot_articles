from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext


from app.loader import dp, UserState


@dp.message_handler(commands="reg")
async def command_reg_handler(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n Пройди регистрацию /reg\n Если не знаешь для чего она - 🖕')
    await message.answer("Введите своё имя")

    await UserState.name.set()
