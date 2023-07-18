import logging
from loguru import logger
import requests
import re
from aiogram.dispatcher import filters
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from app.loader import dp, bot
from app.config import USERS, HEADERS, PAYLOAD, conf
from app.utils.module import *


cb = CallbackData("post", "post2", "id", "action")


@dp.callback_query_handler(cb.filter(), filters.IDFilter(user_id=USERS))
async def callbacks(callback: types.CallbackQuery):
    call = callback.data.split(':')
    post = dict()
    post['type'] = str(call[1])
    post['id'] = call[2]
    post['action'] = str(call[3])

    if post['action'] == 'ping':
        pprint(post)
        # response_list = ping(post['id'], count=1)
        return await callback.answer(
            # text=f'Код - {response_list}',
            # show_alert=True
        )

    if post['action'] == 'photo':
        photos = get_photo_by_id(post['id'])
        if photos:
            await send_photo_by_id(callback, photos)
        else:
            await callback.answer(
                text=f'Фотографии не найдены',
                show_alert=True
            )
        return True

    await bot.send_message(callback.from_user.id, f"type: {post['type']}\nid: {post['id']}\naction: {post['action']}")
    await callback.answer()


@dp.message_handler(filters.IDFilter(user_id=USERS), content_types=types.ContentType.PHOTO)
async def scan_message(message: types.Message):
    logger.debug("Downloading photo")
    # file_info = await bot.get_file(message.photo[-1].file_id)
    if message.reply_to_message:
        if re.match('^\\d{5}$', message.reply_to_message.text):
            text = re.search('^\\d{5}$', message.reply_to_message.text)
            text = str(text[0])

            filename = text + '-' + message.photo[-1].file_unique_id + '.jpg'
            await message.photo[-1].download(destination_file='../photos/' + filename)

            await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text)
            await message.answer("Принято")
            logger.debug("Downloading photo")

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

            if iterator['status']['label'] == 'Active':
                status = '🟢'
            elif iterator['status']['label'] == 'Offline':
                status = '🪦'
            elif iterator['status']['label'] == 'Inventory':
                status = '📦'
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
                # types.InlineKeyboardButton(text="Ping", callback_data=cb.new(post2="ip", action="ping", id=ip)),
                types.InlineKeyboardButton(text="Фото", callback_data=cb.new(post2="device", action="photo", id=did))
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            keyboard.add(*buttons)

            await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer("Ничего не найдено")
