from aiogram.dispatcher.filters.state import StatesGroup, State


class PhotoDownload(StatesGroup):
    photo = State()
    id = State()
    address = State()
