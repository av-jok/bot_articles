from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext


from app.loader import dp, UserState


@dp.message_handler(commands="reg")
async def command_reg_handler(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\n Пройди регистрацию /reg\n Если не знаешь для чего она - 🖕')
    await message.answer("Введите своё имя")
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Отлично! Теперь введите ваш адрес.")
    await UserState.next()  # либо же UserState.adress.set()


@dp.message_handler(state=UserState.address)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data['username']}\n"
                         f"Адрес: {data['address']}")
    await state.finish()
