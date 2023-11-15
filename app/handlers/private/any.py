import logging
from loguru import logger
import re
import os
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import filters
from aiogram import types
from app.loader import dp, bot, query_select, query_insert
from app.config import USERS, HEADERS, conf, upload_dir_photo, upload_dir_data, Switch
from requests import request

cb = CallbackData("post", "id", "action")
sw = Switch()


async def send_photo_by_id(callback: types.CallbackQuery, photos, photos2):
    media = types.MediaGroup()

    if photos is not None:
        for iterator in photos:
            img_data = request("GET", iterator['image'], headers=HEADERS, data='').content
            filename = upload_dir_data + str(iterator['object_id']) + "_" + str(iterator['pid']) + ".jpg"
            with open(filename, 'wb') as photo:
                photo.write(img_data)
            media.attach_photo(types.InputFile(filename, iterator['name']))

    if photos2 is not None:
        for iterator in photos2:
            filename = upload_dir_photo + str(iterator['name'])
            media.attach_photo(types.InputFile(filename, iterator['name']))

    await types.ChatActions.upload_photo()
    await callback.message.reply_media_group(media=media)
    await callback.answer()

    return True


@dp.callback_query_handler(cb.filter(), filters.IDFilter(user_id=USERS))
async def callbacks(callback: types.CallbackQuery, callback_data: dict):
    post = dict()
    post['id'] = callback_data.get('id')
    post['action'] = callback_data.get('action')
    switch = sw(post['id'])

    if post['action'] == 'photo':
        if switch.images or switch.images2:
            await send_photo_by_id(callback, switch.images, switch.images2)
            await callback.answer()
        else:
            await callback.answer(text="Фотографии не найдены", show_alert=True)
        return True

    if post['action'] == 'ping':
        hostname = switch.ip
        host = "is down!"
        response = os.system("ping -c 1 -W 1 " + hostname + "> /dev/null")
        if response == 0:
            host = "is up!"

        await bot.send_message(callback.from_user.id, f"Switch: {switch.name} {host}", reply_to_message_id=callback.message.message_id)
        await callback.answer()
        return True

    await bot.send_message(callback.from_user.id, f"type: {post['type']}\nid: {post['id']}\naction: {post['action']}")
    await callback.answer()


# @rate_limit(1)
@dp.message_handler(filters.IDFilter(user_id=USERS), content_types=types.ContentType.PHOTO)
async def scan_message(message: types.Message):
    if message.reply_to_message and re.match('^\\d{5}$', message.reply_to_message.text):
        is_exist = False
        text = re.search('^\\d{5}$', message.reply_to_message.text)
        text = str(text[0])
        # switch = sw('id')

        filename = text + '-' + message.photo[-1].file_unique_id + '.jpg'
        text_out = (f"Инв № - {text}\n"
                    f"Файл - {filename}\n"
                    f"Отправил - {message.reply_to_message.from_user.first_name}"
                    )
        select_all_rows = f"SELECT * FROM `bot_photo` WHERE tid='{message.photo[-1].file_unique_id}' AND sid='{text}' LIMIT 1"
        row = query_select(select_all_rows)

        if not row:
            insert_query = f"INSERT INTO `bot_photo` (`sid`, `name`, `tid`, `file_id`, `upload`) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}', '{message.photo[-1].file_id}',{message.reply_to_message.from_user.first_name});"
            query_insert(insert_query)
            is_exist = True
            logger.debug(f"is_exist = {is_exist}")

        await message.photo[-1].download(destination_file=upload_dir_photo + filename)
        destination = upload_dir_photo + filename
        image_id = message.photo[len(message.photo) - 1].file_id
        file_path = (await bot.get_file(image_id)).file_path
        await bot.download_file(file_path, destination)

        # buttons = [
        #     types.InlineKeyboardButton(text="Device", url=switch.url),
        #     types.InlineKeyboardButton(text="Фото", callback_data=cb.new(action="photo", id=switch.nid))
        # ]
        # keyboard = types.InlineKeyboardMarkup(row_width=3)
        # keyboard.add(*buttons)

        if is_exist:
            if message.from_user.id != 252810436:
                await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text_out)
            # await message.answer("Принято " + filename)
            await bot.send_message(message.from_user.id, f"Принято {filename}", reply_to_message_id=message.reply_to_message)
        else:
            await message.answer("Такое фото уже есть в базе")
    else:
        await message.answer("Фотография должна быть ответом на Инв свича")


@dp.message_handler(filters.IDFilter(user_id=USERS))
async def echo(message: types.Message):
    if len(message.text) < 4:
        await message.answer("Запрос должен быть длиннее")
        return False

    url = conf.netbox.netbox_url + "api/dcim/devices/?q=" + message.text
    response = request("GET", url, headers=HEADERS, data='')

    json = response.json()

    if json['count'] > 0:
        for iterator in json['results']:
            switch = sw(iterator['id'])

            match switch.status:
                case 'Active':
                    status = '🟢'
                case 'Offline':
                    status = '🔴'
                case 'Inventory':
                    status = '📦'
                case 'Decommissioning':
                    status = '⚰️'
                case _:
                    status = switch.status

            msg = (
                f"Адрес: {switch.address}\n"
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
                types.InlineKeyboardButton(text="Ping", callback_data=cb.new(action="ping", id=switch.nid)),
                types.InlineKeyboardButton(text="Фото", callback_data=cb.new(action="photo", id=switch.nid))
            ]
            logger.debug(f"{switch.nid}")
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer("Ничего не найдено")
