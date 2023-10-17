import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from contextlib import suppress
from aiogram.utils.exceptions import ChatNotFound


logging.basicConfig(level=logging.DEBUG)

'''''
https://api.telegram.org/bot1323680830:AAHMuqFWXGsyYuab9rTXtVfjUYEd1iDm2Xc/getWebhookInfo
https://api.telegram.org/bot1323680830:AAHMuqFWXGsyYuab9rTXtVfjUYEd1iDm2Xc/setWebhook?url=https://psiline.ru/bot/&drop_pending_updates=false
https://api.telegram.org/bot1323680830:AAHMuqFWXGsyYuab9rTXtVfjUYEd1iDm2Xc/deleteWebhook

'''''


bot = Bot(token="1323680830:AAHMuqFWXGsyYuab9rTXtVfjUYEd1iDm2Xc")
dp = Dispatcher(bot)

cd_walk = CallbackData("dun_w", "action", "floor")


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.delete_webhook()

    markup = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(f"Налево",
                             callback_data=cd_walk.new(
                                 action='1',
                                 floor=2
                             ))
    )
    await message.answer("text", reply_markup=markup)


@dp.callback_query_handler(text="button_clicked")
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    inline_kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Первая кнопка!', callback_data='button1'))

    await message.reply("Первая инлайн кнопка", reply_markup=inline_kb)


@dp.callback_query_handler(cd_walk.filter())
async def button_press(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get('action')  # 1 or 2
    floor = callback_data.get('floor')  # 2
    logging.info(f"{action} == {floor}")


async def notify_admins(text: str):
    admins = [252810436]
    count = 0
    for admin in admins:
        with suppress(ChatNotFound):
            await dp.bot.send_message(admin, text)
            count += 1
    logging.info(f"{count} admins received messages")


async def on_startup(dispatcher: Dispatcher) -> False:
    await notify_admins("Bot started")
    return True


async def on_sthutdown(dispatcher: Dispatcher) -> False:
    await notify_admins("Bot shutdown")
    return True

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_sthutdown, skip_updates=True)
