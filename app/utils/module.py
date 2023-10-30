import requests
# from pprint import pprint
# from loguru import logger
from aiogram import types
from app.config import HEADERS, conf
# from app.loader import db


def get_photo_by_id(ids):
    url = conf.misc.netbox_url + "api/extras/image-attachments/?object_id=" + ids
    response = requests.request("GET", url, headers=HEADERS, data='')
    json = response.json()
    photos = list()
    if json['count'] > 0:
        for iterator in json['results']:
            photos.append({
                'pid': iterator['id'],
                'name': iterator['name'],
                'image': iterator['image'],
                'object_id': iterator['object_id']}
            )
        return photos
    else:
        return False

# media = types.MediaGroup()
# onlyfiles = [f for f in listdir('photo') if isfile(join('photo', f))]
# for i in onlyfiles:
#     photo = 'photo/' + i
#     media.attach_photo(photo=types.InputFile(path_or_bytesio=photo))
#
# bk = InlineKeyboardButton(callback_data='start', text='Назад')
# bk = InlineKeyboardMarkup(row_width=2).add(bk)
# await bot.send_media_group(call.from_user.id, media=media)
