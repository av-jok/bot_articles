from loguru import logger
import re
import requests
from pprint import pprint
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import filters
from aiogram import types
from app.loader import db, dp, bot
from app.middlewares import rate_limit
from app.config import USERS, HEADERS, PAYLOAD, conf, upload_dir_photo
from app.utils.module import get_photo_by_id, send_photo_by_id, send_photo_in_base

cb = CallbackData("post", "post2", "id", "action")


@dp.callback_query_handler(cb.filter(), filters.IDFilter(user_id=USERS))
async def callbacks(callback: types.CallbackQuery):
    # media = types.MediaGroup()
    call = callback.data.split(':')
    post = dict()
    post['type'] = str(call[1])
    post['id'] = call[2]
    post['action'] = str(call[3])

    if post['action'] == 'ping':
        pprint(post)
        return await callback.answer(
            # text=f'Код - {response_list}',
            # show_alert=True
        )

    if post['action'] == 'photo':
        photos = get_photo_by_id(post['id'])
        if photos:
            await send_photo_by_id(callback, photos)
            await send_photo_in_base(post['id'])
        else:
            await callback.answer(
                text=f'Фотографии не найдены',
                show_alert=True
            )
        return True

    await bot.send_message(callback.from_user.id, f"type: {post['type']}\nid: {post['id']}\naction: {post['action']}")
    await callback.answer()


@rate_limit(10)
@dp.message_handler(filters.IDFilter(user_id=USERS), content_types=types.ContentType.PHOTO)
async def scan_message(message: types.Message):
    # file_info = await bot.get_file(message.photo[-1].file_id)
    if message.reply_to_message:
        if re.match('^\\d{5}$', message.reply_to_message.text):
            text = re.search('^\\d{5}$', message.reply_to_message.text)
            text = str(text[0])

            filename = text + '-' + message.photo[-1].file_unique_id + '.jpg'
            text_out = (f"Инв № - {text}\n"
                        f"Файл - {filename}\n"
                        f"Отправил - {message.reply_to_message.from_user.first_name}"
                        )
            logger.debug("Downloading photo start")

            # switch = Switch(text, text)

            with db.cursor() as cursor:
                select_all_rows = f"SELECT * FROM `bot_photo` WHERE tid='{message.photo[-1].file_unique_id}' AND sid='{text}' LIMIT 1"
                cursor.execute(select_all_rows)
                rows = cursor.fetchall()
                if rows:
                    is_exist = False
                else:
                    insert_query = f"INSERT INTO `bot_photo` (sid, name, tid) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}');"
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

            logger.debug("Downloading photo end")

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
    response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
    json = response.json()

    if json['count'] > 0:
        # pprint(json['count'])
        for iterator in json['results']:
            did = iterator['id']
            name = iterator['name'].lower()
            device_type = iterator['device_type']['display']
            rack = ''
            if iterator['asset_tag']:
                asset_tag = re.findall(r'\d+', iterator['asset_tag'])
                asset_tag = int(asset_tag[0])
            else:
                asset_tag = None
            if iterator['rack'] is not None:
                rack = False

            if iterator['status']['label'] == 'Active':
                status = '🟢'
            elif iterator['status']['label'] == 'Offline':
                status = '🔴'
            elif iterator['status']['label'] == 'Inventory':
                status = '📦'
            elif iterator['status']['label'] == 'Decommissioning':
                status = '⚰️'
            else:
                status = iterator['status']['label']

            if iterator['primary_ip'] is not None:
                ip = iterator['primary_ip']['address'].split('/')
                ip = ip[0]
            else:
                ip = None
            if iterator['rack']:
                rack = iterator['rack']['name']

            msg = (
                f"Адрес: {iterator['site']['name']}\n"
                f"{rack}\n\n"
                f"Имя: {name} {status}\n"
                f"Инв № : {asset_tag}\n"
                f"{device_type}\n"
                f"{ip}\n\n"
                f"{iterator['comments']}"
            )
            buttons = [
                types.InlineKeyboardButton(text="Device", url=iterator['url'].replace('/api/', '/')),
                # types.InlineKeyboardButton(text="Стойка", callback_data=cb.new(post2="photo", action="svg", id=did)),
                # types.InlineKeyboardButton(text="Ping", callback_data=cb.new(post2="ip", action="ping", id=ip)),
                types.InlineKeyboardButton(text="Фото", callback_data=cb.new(post2="device", action="photo", id=did))
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer("Ничего не найдено")
