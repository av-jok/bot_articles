from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hcode

from app.loader import dp
from app.loader import bot
from app.config import commands
import logging
import app.utils.module as module
from app.middlewares import rate_limit

cb = CallbackData("post", "id", "action")


@dp.message_handler(CommandStart())
async def command_start_handler(msg: types.Message):
    await msg.answer(f'Привет, {msg.from_user.full_name}!\n Пройди регистрацию /reg\n Если не знаешь для чего она - 🖕')


@dp.message_handler(commands="reg")
async def command_reg_handler(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id} \n\n Вы знаете кому его отправить")


@rate_limit(5, "help")
@dp.message_handler(commands="help")
async def command_help_handler(message: types.Message):
    """Responds to /help with list of available commands, which're located in data/config.py"""

    # Generates a list
    answer = ["Available commands: "]
    for command, description in commands:
        answer.append(hcode(f"/{command}") + f" — {description}")

    await message.answer("\n".join(answer), reply_markup=get_keyboard_fab(15555))


def get_keyboard_fab(ids):

    buttons = [
        types.InlineKeyboardButton(text="NetBox", callback_data=cb.new(action="open", id=str(ids))),
        types.InlineKeyboardButton(text="Ping", callback_data=cb.new(action="ping", id=str(ids))),
        types.InlineKeyboardButton(text="Фото", callback_data=cb.new(action="photo", id=2))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    return keyboard


# @dp.callback_query_handler(cb.filter(), filters.IDFilter(user_id=users))
@dp.callback_query_handler(cb.filter())
async def callbacks(callback: types.CallbackQuery):
    logging.info(callback.data)
    call = callback.data.split(':')
    post = dict()
    post['id'] = call[1]
    post['action'] = str(call[2])

    # if post['action'] == 'ping':
    #     response_list = ping(post['id'], count=1)
    #     return await callback.answer(
    #         text=f'Код - {response_list}',
    #         show_alert=True
    #     )

    if post['action'] == 'photo':
        photos = module.get_photo_by_id(post['id'])
        # pprint(photos)
        if photos:
            await module.send_photo_by_id(callback, photos)
        else:
            await callback.answer(
                text=f'Фотографии не найдены',
                show_alert=True
            )
        return True

    # await callback.answer(
    #     text=f'Нажата инлайн кнопка! code={code}\n Код - {ids}',
    #     show_alert=True
    # )

    await bot.send_message(callback.from_user.id, f"type: id: {post['id']}\naction: {post['action']}")
    await callback.answer()
