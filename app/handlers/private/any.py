import logging
# from loguru import logger
import re
# import requests
from aiogram.dispatcher import filters
# from aiogram import types
# import aspose.words as aw

from aiogram.utils.callback_data import CallbackData
from app.loader import dp, bot, db
from app.config import *
from app.utils.module import *


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

    # if post['action'] == 'svg':
    #     url = conf.misc.netbox_url + "api/dcim/devices/" + post['id'] + "/"
    #     response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
    #     json = response.json()
    #     if json['rack'] is not None:
    #         # print(json['rack'])
    #         list_type = ["front", "rear"]
    #         for iterator in list_type:
    #             rack = str(json['rack']['id'])
    #             side = iterator
    #             url = conf.misc.netbox_url + f"api/dcim/racks/{rack}/elevation/?face={side}&render=svg"
    #             response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD).content
    #
    #             filename = f"{rack}_{side}.png"
    #
    #             logger.debug("Start svg2png")
    #             doc = aw.Document()
    #             builder = aw.DocumentBuilder(doc)
    #             shape = builder.insert_image(response)
    #             pagesetup = builder.page_setup
    #             pagesetup.page_width = shape.width
    #             pagesetup.page_height = shape.height
    #             pagesetup.top_margin = 0
    #             pagesetup.left_margin = 0
    #             pagesetup.bottom_margin = 0
    #             pagesetup.right_margin = 0
    #             doc.save("../Rack/" + filename)
    #             logger.debug("End svg2png")
    #
    #             media.attach_photo(types.InputFile("../Rack/" + filename, side))
    #
    #         await types.ChatActions.upload_photo()
    #         await callback.message.reply_media_group(media=media)
    #         await callback.answer()
    #
    #     else:
    #         return await callback.answer(
    #             text=f'Оборудование не привязано к стойке',
    #             show_alert=True
    #         )
    #
    #     #     for iterator in json['results']:
    #     #         did = iterator['id']
    #
    #     return await callback.answer(
    #         # text=f'Код - {response_list}',
    #         # show_alert=True
    #         # cairosvg.svg2pdf(url='image.svg', write_to='image.pdf')
    #     )

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
            text_out = (f"Инв № - {text}\n"
                        f"Файл - {filename}\n"
                        f"Отправил - {message.reply_to_message.from_user.first_name}"
                        )
            logger.debug("Downloading photo start")

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
                    except Exception as ex:
                        print("Error...")
                        print(ex)
                    is_exist = True

            downloaded_file = bot.download_file(bot.get_file(message.photo[len(message.photo) - 1].file_id))
            # src = '../photos/' + filename
            # with open(src, 'wb') as new_file:
            #     new_file.write(downloaded_file)
            # select all data from table

            await message.photo[-1].download(destination_file='../photos/' + filename)
            await download_file(downloaded_file, filename, message)
            logger.debug("Downloading photo end")
            if is_exist:
                await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text_out)
                # await bot.send_message('252810436', caption=text)
                # await message.forward('252810436')
                await message.answer("Принято " + filename)
            else:
                await message.answer("Такое фото уже есть в базе")
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


async def download_file(file: types.File, name: str, message: types.Message):
    logging.info(file)
    destination = r"../photos/" + name
    image_id = message.photo[len(message.photo) - 1].file_id
    file_path = (await bot.get_file(image_id)).file_path

    await bot.download_file(file_path, destination)
