from loguru import logger
import re
from typing import List
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import filters
from aiogram import types
from app.loader import db, dp, bot
from app.middlewares import rate_limit
from app.config import USERS, HEADERS, conf, upload_dir_photo, upload_dir_data, Switch
from requests import request
from pprint import pprint

cb = CallbackData("post", "post2", "id", "action")
sw = Switch(db)


async def send_photo_by_id(callback: types.CallbackQuery, photos, photos2):
    media = types.MediaGroup()

    for iterator in photos:
        img_data = request("GET", iterator['image'], headers=HEADERS, data='').content
        filename = upload_dir_data + str(iterator['object_id']) + "_" + str(iterator['pid']) + ".jpg"
        with open(filename, 'wb') as photo:
            photo.write(img_data)
        media.attach_photo(types.InputFile(filename, iterator['name']))

    for iterator in photos2:
        filename = upload_dir_photo + str(iterator['name'])
        pprint(filename)
        media.attach_photo(types.InputFile(filename, iterator['name']))

    await types.ChatActions.upload_photo()
    await callback.message.reply_media_group(media=media)
    await callback.answer()

    return True


@dp.callback_query_handler(cb.filter(), filters.IDFilter(user_id=USERS))
async def callbacks(callback: types.CallbackQuery):
    # media = types.MediaGroup()
    call = callback.data.split(':')
    post = dict()
    post['type'] = str(call[1])
    post['id'] = call[2]
    post['action'] = str(call[3])

    switch = sw(post['id'])
    # pprint(switch.images)
    # pprint(switch.images2)

    if post['action'] == 'photo':
        if switch.images or switch.images2:
            await send_photo_by_id(callback, switch.images, switch.images2)
        else:
            await callback.answer(
                text=f'Фотографии не найдены',
                show_alert=True
            )
        return True

    await bot.send_message(callback.from_user.id, f"type: {post['type']}\nid: {post['id']}\naction: {post['action']}")
    await callback.answer()


# @dp.message_handler(content_types=types.ContentType.ANY)
# async def handle_albums(message: types.Message, album: List[types.Message]):
#     """This handler will receive a complete album of any type."""
#     media_group = types.MediaGroup()
#     for obj in album:
#         if obj.photo:
#             file_id = obj.photo[-1].file_id
#         else:
#             file_id = obj[obj.content_type].file_id
#
#         try:
#             We can also add a caption to each file by specifying `"caption": "text"`
#             media_group.attach({"media": file_id, "type": obj.content_type})
#         except ValueError:
#             return await message.answer("This type of album is not supported by aiogram.")
#
#     await message.answer_media_group(media_group)


@rate_limit(30)
@dp.message_handler(filters.IDFilter(user_id=USERS), content_types=types.ContentType.PHOTO)
async def scan_message(message: types.Message):
    if message.reply_to_message:
        if re.match('^\\d{5}$', message.reply_to_message.text):
            text = re.search('^\\d{5}$', message.reply_to_message.text)
            text = str(text[0])

            filename = text + '-' + message.photo[-1].file_unique_id + '.jpg'
            text_out = (f"Инв № - {text}\n"
                        f"Файл - {filename}\n"
                        f"Отправил - {message.reply_to_message.from_user.first_name}"
                        )
            # logger.debug("Downloading photo start")
            # switch = Switch(text, text)

            pprint(message.photo[-1])

            with db.cursor() as cursor:
                select_all_rows = f"SELECT * FROM `bot_photo` WHERE tid='{message.photo[-1].file_unique_id}' AND sid='{text}' LIMIT 1"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
                if rows:
                    is_exist = False
                else:
                    insert_query = f"INSERT INTO `bot_photo` (sid, name, tid, file_id) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}', '{message.photo[-1].file_id}');"
                    cursor.execute(insert_query)
                    try:
                        db.commit()
                        is_exist = True
                    except Exception as ex:
                        logger.debug(ex)

            await message.photo[-1].download(destination_file=upload_dir_photo + filename)
            destination = upload_dir_photo + filename
            image_id = message.photo[len(message.photo) - 1].file_id
            file_path = (await bot.get_file(image_id)).file_path
            await bot.download_file(file_path, destination)

            if is_exist:
                if message.from_user.id != 252810436:
                    await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text_out)
                    # await bot.send_message('252810436', caption=text)
                    # await message.forward('252810436')
                await message.answer("Принято " + filename)
            else:
                await message.answer("Такое фото уже есть в базе")

            # logger.debug("Downloading photo end")

        else:
            await message.answer("Фотография должна быть ответом на Инв свича")
    else:
        await message.answer("Фотография должна быть ответом на Инв свича")


@dp.message_handler(filters.IDFilter(user_id=USERS))
async def echo(message: types.Message):
    if len(message.text) < 4:
        await message.answer("Запрос должен быть длиннее")
        return False

    url = conf.misc.netbox_url + "api/dcim/devices/?q=" + message.text
    response = request("GET", url, headers=HEADERS, data='')

    json = response.json()

    if json['count'] > 0:
        for iterator in json['results']:

            switch = sw(iterator['id'])

            if switch.status == 'Active':
                status = '🟢'
            elif switch.status == 'Offline':
                status = '🔴'
            elif switch.status == 'Inventory':
                status = '📦'
            elif switch.status == 'Decommissioning':
                status = '⚰️'
            else:
                status = switch.status

            msg = (
                f"Адрес: {switch.name}\n"
                f"{switch.rack}\n\n"
                f"Имя: {switch.name} {status}\n"
                f"Инв № : {switch.id}\n"
                f"{switch.device_type}\n"
                f"{switch.ip}\n\n"    
                f"{switch.comments}"
            )

            buttons = [
                types.InlineKeyboardButton(text="Device", url=switch.url),
                # types.InlineKeyboardButton(text="Стойка", callback_data=cb.new(post2="photo", action="svg", id=did)),
                # types.InlineKeyboardButton(text="Ping", callback_data=cb.new(post2="ip", action="ping", id=ip)),
                types.InlineKeyboardButton(text="Фото", callback_data=cb.new(post2="device", action="photo", id=switch.nid))
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer("Ничего не найдено")
