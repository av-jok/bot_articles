from typing import List
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from app.loader import dp


class PhotoDownload(StatesGroup):
    photo = State()
    id = State()
    address = State()


# обработчик выхода из машины состояний
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Добавление фото отменено!')


@dp.message_handler(commands="file")
async def command_reg_handler(message: types.Message):
    await message.answer("Введите инвентарный №")
    await PhotoDownload.id.set()


@dp.message_handler(state=PhotoDownload.id)
async def get_street(message: types.Message, state: FSMContext):
    await state.update_data(id=message.text)
    await message.answer("Отлично! Теперь введите адрес.")
    await PhotoDownload.address.set()  # либо же UserState.adress.set()


@dp.message_handler(state=PhotoDownload.address)
async def get_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await message.answer("Отлично! Теперь кидай фото.")
    await PhotoDownload.photo.set()  # либо же UserState.adress.set()


# @dp.message_handler(state=PhotoDownload.photo)
# async def get_address(message: types.Message, state: FSMContext):
#     await state.update_data(address=message.text)
#     data = await state.get_data()
#     await message.answer(f"Инв: {data['id']}\n"
#                          f"Адрес: {data['address']}\n"
#                          f"Фото: {data['photo']}\n"
#                          )
#     await state.finish()

@dp.message_handler(state=PhotoDownload.photo)
async def handle_albums(message: types.Message, state: FSMContext, album: List[types.Message]):
    """This handler will receive a complete album of any type."""
    await state.update_data(photo=message.photo[0].file_id)
    data = await state.get_data()
    media_group = types.MediaGroup()

    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")

    await message.answer(f"Инв: {data['id']}\n"
                         f"Адрес: {data['address']}\n"
                         f"Фото: {data['photo']}\n"
                         )
    await message.answer_media_group(media_group)
    await state.finish()


# @dp.message_handler(state=PhotoDownload.photo)
# async def process_photo(message: types.Message, state: FSMContext):
#
#     await state.update_data(photo=message.photo[0].file_id)
#     data = await state.get_data()
#     await message.answer(f"Инв: {data['id']}\n"
#                          f"Адрес: {data['address']}\n"
#                          f"Фото: {data['photo']}\n"
#                          )
#     await state.finish()
