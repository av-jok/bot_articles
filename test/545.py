# ОБЪЯВЛЕНИЕ ВСЕХ ПЕРЕМЕННЫХ И ТД
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from random import randint

TOKEN_API = " "  # ТОКЕН

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)


# НАЧАЛО ОФИГЕТЬ КАКОГО БОЛЬШОГО КОДА И ФСМа
class states(StatesGroup):
    check_result = State()


# ОБЪЯВЛЕНИE ИНЛАЙН КЛАВИАТУР


# ОБЪЯВЛЕНИE КЛАВИАТУР
kb0 = ReplyKeyboardMarkup(resize_keyboard=True)
btn0 = KeyboardButton('Выбрать тему')
kb0.add(btn0)

kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton('Теория §1')
btn2 = KeyboardButton('Примеры §1')
btn3 = KeyboardButton('Задания §1')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb1.add(btn1).insert(btn2).add(btn3).add(btn4)

kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
btn11 = KeyboardButton('Теория §2')
btn22 = KeyboardButton('Примеры §2')
btn33 = KeyboardButton('Задания §2')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb2.add(btn11).insert(btn22).add(btn33).add(btn4)

kb3 = ReplyKeyboardMarkup(resize_keyboard=True)
btn111 = KeyboardButton('Теория §3')
btn222 = KeyboardButton('Примеры §3')
btn333 = KeyboardButton('Задания §3')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb3.add(btn111).insert(btn222).add(btn333).add(btn4)

kb4 = ReplyKeyboardMarkup(resize_keyboard=True)
btn1111 = KeyboardButton('Теория §4')
btn2222 = KeyboardButton('Примеры §4')
btn3333 = KeyboardButton('Задания §4')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb4.add(btn1111).insert(btn2222).add(btn3333).add(btn4)

kb5 = ReplyKeyboardMarkup(resize_keyboard=True)
btn11111 = KeyboardButton('Теория §5')
btn22222 = KeyboardButton('Примеры §5')
btn33333 = KeyboardButton('Задания §5')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb5.add(btn11111).insert(btn22222).add(btn33333).add(btn4)

kb6 = ReplyKeyboardMarkup(resize_keyboard=True)
btn111111 = KeyboardButton('Теория §6')
btn222222 = KeyboardButton('Примеры §6')
btn333333 = KeyboardButton('Задания §6')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb6.add(btn111111).insert(btn222222).add(btn333333).add(btn4)

kb7 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn4 = KeyboardButton('Вернуться к выбору темы')
kb7.add(btn4)

kb8 = ReplyKeyboardMarkup(resize_keyboard=True)
btn3 = KeyboardButton('Задания §1')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb8.add(btn3).add(btn4)

kb9 = ReplyKeyboardMarkup(resize_keyboard=True)
btn33 = KeyboardButton('Задания §2')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb9.add(btn33).add(btn4)

kb10 = ReplyKeyboardMarkup(resize_keyboard=True)
btn333 = KeyboardButton('Задания §3')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb10.add(btn333).add(btn4)

kb11 = ReplyKeyboardMarkup(resize_keyboard=True)
btn3333 = KeyboardButton('Задания §4')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb11.add(btn3333).add(btn4)

kb12 = ReplyKeyboardMarkup(resize_keyboard=True)
btn33333 = KeyboardButton('Задания §5')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb12.add(btn33333).add(btn4)

kb13 = ReplyKeyboardMarkup(resize_keyboard=True)
btn333333 = KeyboardButton('Задания §6')
btn4 = KeyboardButton('Вернуться к выбору темы')
kb13.add(btn333333).add(btn4)


# СТАРТ
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Привет! Я бот помогающий в изучении математики! Чтобы выбрать тему для её дальнейшего изучения - нажмите на кнопку!",
                           parse_mode="HTML",
                           reply_markup=kb0)  # ВОЗВРАЩАЕМ КЛАВИАТУРУ kb0


# ОТВЕТ НА КНОПКИ ПОЛЬЗОВАТЕЛЯ

# ХЕНДЛЕРЫ С КНОПКАМИ ИНЛАЙН
@dp.message_handler(text="Выбрать тему")  # ХЕНДЛЕР НА ОБРАБОТКУ kb0
async def vote_command(message: types.Message):
    in_lkb0 = InlineKeyboardMarkup(row_width=1)  # 2
    inl_btn0 = InlineKeyboardButton(text='Арифметический квадратный корень', callback_data="tema1")
    inl_btn1 = InlineKeyboardButton(text='Свойства квадратных корней', callback_data="tema2")
    inl_btn2 = InlineKeyboardButton(text='Применение свойств квадратных корней', callback_data="tema3")
    inl_btn3 = InlineKeyboardButton(text='Линейные неравенства с одной переменной', callback_data="tema4")
    inl_btn4 = InlineKeyboardButton(text='Квадратные уравнения', callback_data="tema5")
    inl_btn5 = InlineKeyboardButton(text='Теорема Виета', callback_data="tema6")
    in_lkb0.add(inl_btn0, inl_btn1, inl_btn2, inl_btn3, inl_btn4, inl_btn5)

    await message.reply("Темы, которые вы можете выбрать:",
                        reply_markup=in_lkb0)


@dp.message_handler(text="Вернуться к выбору темы")
async def vote_command(message: types.Message):
    INLkb0 = InlineKeyboardMarkup(row_width=1)  # 2
    inl_btn0 = InlineKeyboardButton(text='Арифметический квадратный корень', callback_data="tema1")
    inl_btn1 = InlineKeyboardButton(text='Свойства квадратных корней', callback_data="tema2")
    inl_btn2 = InlineKeyboardButton(text='Применение свойств квадратных корней', callback_data="tema3")
    inl_btn3 = InlineKeyboardButton(text='Линейные неравенства с одной переменной', callback_data="tema4")
    inl_btn4 = InlineKeyboardButton(text='Квадратные уравнения', callback_data="tema5")
    inl_btn5 = InlineKeyboardButton(text='Теорема Виета', callback_data="tema6")
    INLkb0.add(inl_btn0, inl_btn1, inl_btn2, inl_btn3, inl_btn4, inl_btn5)

    await message.reply("Темы, которые вы можете выбрать:",
                        reply_markup=INLkb0)


# ОБРАБОТКА КАЛБЕКОВ
@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'tema1':
        await bot.send_message(callback.from_user.id,
                               'В этом разделе, вы можете проверить свои знания. Узнать что-то новое, повторить теорию!',
                               reply_markup=kb1)
    if callback.data == 'tema2':
        await bot.send_message(callback.from_user.id,
                               'В этом разделе, вы можете проверить свои знания. Узнать что-то новое, повторить теорию!',
                               reply_markup=kb2)
    if callback.data == 'tema3':
        await bot.send_message(callback.from_user.id,
                               'В этом разделе, вы можете проверить свои знания. Узнать что-то новое, повторить теорию!',
                               reply_markup=kb3)
    if callback.data == 'tema4':
        await bot.send_message(callback.from_user.id,
                               'В этом разделе, вы можете проверить свои знания. Узнать что-то новое, повторить теорию!',
                               reply_markup=kb4)
    if callback.data == 'tema5':
        await bot.send_message(callback.from_user.id,
                               'В этом разделе, вы можете проверить свои знания. Узнать что-то новое, повторить теорию!',
                               reply_markup=kb5)
    if callback.data == 'tema6':
        await bot.send_message(callback.from_user.id,
                               'В этом разделе, вы можете проверить свои знания. Узнать что-то новое, повторить теорию!',
                               reply_markup=kb6)


# ОТСЫЛКА ЗАДАНИЙ
@dp.message_handler(text="Задания §1")
async def btn(message: types.Message, state: FSMContext):
    await message.reply("Выполните задание или вернитесь к выбору темы",
                        reply_markup=kb7)
    list_zad1 = [
    ]

    list_answear1 = [
    ]
    randNum = randint(0, len(list_zad1) - 1)
    await bot.send_photo(message.chat.id, list_zad1[randNum])
    await state.update_data(correct_result=list_answear1[randNum])
    await states.check_result.set()


@dp.message_handler(text="Задания §2")
async def btn(message: types.Message, state: FSMContext):
    await message.reply("Выполните задание или вернитесь к выбору темы",
                        reply_markup=kb7)
    list_zad2 = [
    ]

    list_answear2 = [
    ]
    randNum = randint(0, len(list_zad2) - 1)
    await bot.send_photo(message.chat.id, list_zad2[randNum])
    await state.update_data(correct_result=list_answear2[randNum])
    await states.check_result.set()


@dp.message_handler(text="Задания §3")
async def btn(message: types.Message, state: FSMContext):
    await message.reply("Выполните задание или вернитесь к выбору темы",
                        reply_markup=kb7)
    list_zad3 = [

    ]

    list_answear3 = [

    ]
    randNum = randint(0, len(list_zad3) - 1)
    await bot.send_photo(message.chat.id, list_zad3[randNum])
    await state.update_data(correct_result=list_answear3[randNum])
    await states.check_result.set()


@dp.message_handler(text="Задания §4")
async def btn(message: types.Message, state: FSMContext):
    await message.reply("Выполните задание или вернитесь к выбору темы",
                        reply_markup=kf)
    list_zad4 = [

    ]

    list_answear4 = [

    ]
    randNum = randint(0, len(list_zad4) - 1)
    await bot.send_photo(message.chat.id, list_zad4[randNum])
    await state.update_data(correct_result=list_answear4[randNum])
    await states.check_result.set()


@dp.message_handler(text="Задания §5")
async def btn(message: types.Message, state: FSMContext):
    await message.reply("Выполните задание или вернитесь к выбору темы",
                        reply_markup=kb7)
    list_zad5 = [

    ]

    list_answear5 = [

    ]
    randNum = randint(0, len(list_zad5) - 1)
    await bot.send_photo(message.chat.id, list_zad5[randNum])
    await state.update_data(correct_result=list_answear5[randNum])
    await states.check_result.set()


@dp.message_handler(text="Задания §6")
async def btn(message: types.Message, state: FSMContext):
    await message.reply("Выполните задание или вернитесь к выбору темы",
                        reply_markup=kb7)
    list_zad6 = [

    ]

    list_answear6 = [

    ]
    randNum = randint(0, len(list_zad6) - 1)
    await bot.send_photo(message.chat.id, list_zad6[randNum])
    await state.update_data(correct_result=list_answear6[randNum])
    await states.check_result.set()


# ПРОВЕРКА ОТВЕТОВ ПОЛЬЗОВАТЕЛЯ
@dp.message_handler(state=states.check_result)
async def checking_result(message: types.Message, state: FSMContext):
    await state.update_data(user_answear=message.text)
    data = await state.get_data()
    try:
        if data['correct_result'] == int(data['user_answear']):
            await message.answer("Правильно, вы молодец! Выберите следующее действие:",
                                 reply_markup=x)  # Вместо х - значение клавиатуры
        else:
            INLkb0 = InlineKeyboardMarkup(row_width=1)  # 2
            inl_btn0 = InlineKeyboardButton(text='Арифметический квадратный корень', callback_data="tema1")
            inl_btn1 = InlineKeyboardButton(text='Свойства квадратных корней', callback_data="tema2")
            inl_btn2 = InlineKeyboardButton(text='Применение свойств квадратных корней', callback_data="tema3")
            inl_btn3 = InlineKeyboardButton(text='Линейные неравенства с одной переменной', callback_data="tema4")
            inl_btn4 = InlineKeyboardButton(text='Квадратные уравнения', callback_data="tema5")
            inl_btn5 = InlineKeyboardButton(text='Теорема Виета', callback_data="tema6")
            INLkb0.add(inl_btn0, inl_btn1, inl_btn2, inl_btn3, inl_btn4, inl_btn5)
            await message.reply("Неправильно, попробуйте ещё раз!")
            await message.answer("Вы были возвращены в меню. Выберите тему", reply_markup=INLkb0)

    except ValueError:
        if data['correct_result'] == data['user_answear']:
            await message.reply("Правильно, вы молодец! Выберите следующее действие:",
                                reply_markup=kb7)
        else:
            INLkb0 = InlineKeyboardMarkup(row_width=1)  # 2
            inl_btn0 = InlineKeyboardButton(text='Арифметический квадратный корень', callback_data="tema1")
            inl_btn1 = InlineKeyboardButton(text='Свойства квадратных корней', callback_data="tema2")
            inl_btn2 = InlineKeyboardButton(text='Применение свойств квадратных корней', callback_data="tema3")
            inl_btn3 = InlineKeyboardButton(text='Линейные неравенства с одной переменной', callback_data="tema4")
            inl_btn4 = InlineKeyboardButton(text='Квадратные уравнения', callback_data="tema5")
            inl_btn5 = InlineKeyboardButton(text='Теорема Виета', callback_data="tema6")
            INLkb0.add(inl_btn0, inl_btn1, inl_btn2, inl_btn3, inl_btn4, inl_btn5)
            await message.answer("Вы были возвращены в меню. Выберите тему", reply_markup=INLkb0)

    await state.finish()


# ОТПРАВКА ТЕОРИИ
@dp.message_handler(text="Теория §1")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Теория §2")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Теория §3")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Теория §4")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Теория §5")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Теория §6")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


# ОТПРАВКА *ПРИМЕРОВ*
@dp.message_handler(text="Примеры §1")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Примеры §2")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Примеры §3")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Примеры §4")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Примеры §5")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


@dp.message_handler(text="Примеры §6")
async def btn(message: types.Message, state: FSMContext):
    await bot.send_photo(chat_id=message.chat.id, photo='')


# ЦЕ КОНЕЦ
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
