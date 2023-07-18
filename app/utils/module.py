import requests
from pprint import pprint
from aiogram import types
from app.config import USERS, HEADERS, PAYLOAD, conf


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
        # pprint(iterator['image'])
        img_data = requests.get(iterator['image']).content
        filename = "../data/" + str(iterator['object_id']) + "_" + str(iterator['pid']) + ".jpg"
        with open(filename, 'wb') as photo:
            photo.write(img_data)
        media.attach_photo(types.InputFile(filename, iterator['name']))

    await types.ChatActions.upload_photo()
    await callback.message.reply_media_group(media=media)

    return True
