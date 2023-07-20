from aiogram import types
from app.loader import dp


@dp.message_handler(commands="reg")
async def command_reg_handler(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id} \n\n Вы знаете кому его отправить")
