from typing import Union

from loguru import logger
from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import StatesGroup, State

from app.loader import dp, bot
from app.config import USERS, conf


# from typing import Union


class NewSwitch(StatesGroup):
    asset_tag = State()
    ipaddress = State()
    serial = State()
    name = State()
    model = State()
    fin = State()


cb = CallbackData("switch", "action", "value")


# buttons = [
#     types.InlineKeyboardButton(text="Device", url=switch.url),
#     types.InlineKeyboardButton(text="Фото", callback_data=cb.new(action="photo", id=switch.nid))
# ]
# keyboard = types.InlineKeyboardMarkup(row_width=3)
# keyboard.add(*buttons)

# обработчик выхода из машины состояний
@dp.message_handler(filters.IDFilter(user_id=USERS), state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('отмена!')


@dp.message_handler(filters.IDFilter(user_id=USERS), commands="new_switch")
async def command_reg_handler(message: types.Message):
    await message.answer("!!! Добавляем новый свитч !!! \nДля отмены ввести /cancel")
    await message.answer("Введите инвентарный №")
    await NewSwitch.asset_tag.set()


@dp.message_handler(filters.IDFilter(user_id=USERS), state=NewSwitch.asset_tag)
async def get_street(message: types.Message, state: FSMContext):
    await state.update_data(asset_tag=message.text)
    await message.answer("Введите SN.")
    await NewSwitch.serial.set()  # либо же UserState.adress.set()


@dp.message_handler(filters.IDFilter(user_id=USERS), state=NewSwitch.serial)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Модель свича.")
    await NewSwitch.model.set()  # либо же UserState.adress.set()


@dp.message_handler(filters.IDFilter(user_id=USERS), state=NewSwitch.model)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == '5':
        await state.update_data(name=message.text)
        await NewSwitch.name.set()
        await message.answer("Отлично! Теперь твой возраст.")
    else:
        await NewSwitch.name.set()  # либо же UserState.adress.set()
        await message.answer("Ошибка! Теперь кидай фото.")


@dp.message_handler(filters.IDFilter(user_id=USERS), state=NewSwitch.name)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await NewSwitch.fin.set()
    buttons = [
        types.InlineKeyboardButton(text="Записать", callback_data="send_storage"),
        types.InlineKeyboardButton(text="Отменить", callback_data="cancel")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    data = await state.get_data()
    await bot.send_message(
        message.from_user.id,
        f"{data['asset_tag']}\n{data['address']}\n{data['name']}\n{data['age']}",
        reply_markup=keyboard
    )


@dp.callback_query_handler(filters.IDFilter(user_id=USERS), text='cancel', state=NewSwitch.fin)
async def process_callback(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    print("HERE")
    await call.answer(text="Отмена", show_alert=True)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Отмена!",
        # reply_markup=keyboard
    )


@dp.callback_query_handler(filters.IDFilter(user_id=USERS), text='send_storage', state=NewSwitch.fin)
async def process_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if call.data == "send_storage":
        print(await state.get_data())
        data = await state.get_data()
        await state.finish()
        buttons = [
            types.InlineKeyboardButton(text="Конфиг", callback_data=cb.new(action="send", value="config")),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"{data['asset_tag']}\n{data['address']}\n{data['name']}\n{data['age']}",
            reply_markup=keyboard
        )


@dp.callback_query_handler(filters.IDFilter(user_id=USERS), cb.filter())
async def send_data(call: types.CallbackQuery, callback_data: dict):
    post = dict()
    post['action'] = callback_data.get('action')
    post['value'] = callback_data.get('value')
    await call.answer()

    if callback_data.get('value') == 'config':

        return await bot.send_message(call.from_user.id, f"Здесь будет конфиг")

    await bot.send_message(call.from_user.id, f"value: {post['value']}\naction: {post['action']}")

# @dp.message_handler(state=PhotoDownload.photo)
# async def get_address(message: types.Message, state: FSMContext):
#     await state.update_data(address=message.text)
#     data = await state.get_data()
#     await message.answer(f"Инв: {data['id']}\n"
#                          f"Адрес: {data['address']}\n"
#                          f"Фото: {data['photo']}\n"
#                          )
#     await state.finish()
