import requests
# from pprint import pprint
# from loguru import logger
from aiogram import types
from app.config import HEADERS, PAYLOAD, conf, upload_dir_data
# from app.loader import db


def get_photo_by_id(ids):
    url = conf.misc.netbox_url + "api/extras/image-attachments/?object_id=" + ids
    response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
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


async def send_photo_by_id(callback: types.CallbackQuery, photos):
    media = types.MediaGroup()

    for iterator in photos:

        # img_data = requests.get(iterator['image']).content
        img_data = requests.request("GET", iterator['image'], headers=HEADERS, data=PAYLOAD).content
        filename = upload_dir_data + str(iterator['object_id']) + "_" + str(iterator['pid']) + ".jpg"
        with open(filename, 'wb') as photo:
            photo.write(img_data)
        media.attach_photo(types.InputFile(filename, iterator['name']))

    await types.ChatActions.upload_photo()
    await callback.message.reply_media_group(media=media)
    await callback.answer()

    return True


def send_photo_in_base(pid):
    # TODO Доделать вывод фоток

    # with db.cursor() as cursor:
    #     select_all_rows = "SELECT * FROM `users`"
    #     cursor.execute(select_all_rows)
    #
    #     rows = cursor.fetchall()
    #     for row in rows:
    #         print(row)
    print("#" * 20)
    return pid
