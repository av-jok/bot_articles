import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.callback_data import CallbackData

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token="1323680830:AAHMuqFWXGsyYuab9rTXtVfjUYEd1iDm2Xc")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton(f"Text", callback_data="text")
    )
    await message.answer("text", reply_markup=markup)


@dp.callback_query_handler()
async def button_press(call: CallbackQuery, callback_data: dict):
    action = callback_data.get('action')  # 1 or 2
    floor = callback_data.get('floor')  # 2
    logging.info(f"{action} == {floor}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
