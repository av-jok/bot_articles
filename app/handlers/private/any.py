import re
import os
import time
import pymysql
import pynetbox
import requests
import ipaddress
from typing import Any
from loguru import logger
from pprint import pprint
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher import filters
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.loader import dp, bot, query_insert
from app.config import conf, nb
from requests import request

cb = CallbackData("post", "action", "value", "id")


@dp.callback_query_handler(cb.filter(), filters.IDFilter(user_id=conf.misc.users))
async def callbacks(callback: types.CallbackQuery, callback_data: dict) -> bool:
    post = dict()
    post['action'] = callback_data.get('action')
    post['value'] = callback_data.get('value')
    post['id'] = callback_data.get('id')

    await callback.answer()
    device = nb.dcim.devices.get(id=callback_data.get('value'))

    if callback_data.get('action') == 'upload':
        logger.debug(f"Upload - 1")

        url = conf.netbox.netbox_url
        filename = conf.tg_bot.upload_dir_photo + callback_data.get('id')

        await bot.send_message(callback.from_user.id, f"{url}\n{filename}")
        logger.debug(f"Upload - {url} - {filename}")

        client = requests.session()

        client.get(url)
        csrftoken = client.cookies['csrftoken']
        logger.debug(f"Upload - {csrftoken}")

        login_data = dict(
            username=conf.netbox.netbox_login,
            password=conf.netbox.netbox_pass,
            csrfmiddlewaretoken=csrftoken,
            next=f"/"
        )
        r = client.post(f"{url}/login/", data=login_data, headers=dict(Referer=url))

        csrftoken = r.cookies['csrftoken']
        logger.debug(f"Upload - {csrftoken}")

        res = client.get(
            f"{url}/extras/image-attachments/add/?content_type=19&object_id={device.id}",
            data={'csrftoken': csrftoken, 'csrfmiddlewaretoken': csrftoken},
            headers=dict(Referer=url)
        )

        csrftoken = res.cookies['csrftoken']
        logger.debug(f"Upload - {csrftoken}")

        res = client.post(
            f"{url}/extras/image-attachments/add/?content_type=19&object_id={device.id}",
            files={'image': open(filename, 'rb')},
            data={'name': '', 'csrfmiddlewaretoken': csrftoken},
            headers=dict(Referer=url)
        )
        logger.debug(f"Код ответа - {res.status_code}")
        await bot.send_message(callback.from_user.id, f"Код ответа - {res.status_code}")
        return True

    if callback_data.get('action') == 'photo':
        db = pymysql.connect(host=conf.db.host,
                             user=conf.db.user,
                             password=conf.db.password,
                             database=conf.db.database,
                             # cursorclass=pymysql.cursors.DictCursor
                             )
        with db.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(`sid`) as cnt from bot_photo bp WHERE `sid`={device.asset_tag}")
            cnt_db = cursor.fetchone()
            cnt_db = int(cnt_db[0])

        media = types.MediaGroup()
        cnt_nb = nb.extras.image_attachments.count(object_id=callback_data.get('value'))

        if cnt_nb > 0 or cnt_db > 0:
            logger.debug(f"Фото: в НБ - {cnt_nb}, в БД - {str(cnt_db)}")
            if cnt_nb > 0:
                imgs = nb.extras.image_attachments.filter(object_id=callback_data.get('value'))
                for item in imgs:
                    img_data = request("GET", item.image, headers=conf.misc.headers, data='').content
                    filename = conf.tg_bot.upload_dir_data + str(item.object_id) + "_" + str(item.id) + ".jpg"
                    with open(filename, 'wb') as photo:
                        photo.write(img_data)
                    media.attach_photo(types.InputFile(filename, item.name))
            if cnt_db > 0:
                with db.cursor() as cursor:
                    query = f"SELECT `name` FROM `bot_photo` WHERE sid='{device.asset_tag}'"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                for row in rows:
                    filename = conf.tg_bot.upload_dir_photo + str(row[0])
                    media.attach_photo(types.InputFile(filename, device.name))
                db.close()
                pass

            await types.ChatActions.upload_photo()
            await callback.message.reply_media_group(media=media)
        else:
            logger.debug(f"Фото не найдено")
            await bot.send_message(callback.from_user.id, f"Фотографии не найдены",
                                   reply_to_message_id=callback.message.message_id)
            await callback.answer(text="Фотографии не найдены", show_alert=True)
        return True

    if callback_data.get('action') == 'ping':
        host = "is down!"
        try:
            hostname = ipaddress.ip_interface(device.primary_ip4)
            hostname = str(hostname.ip)
        except ValueError:
            hostname = None

        response = os.system("ping -c 1 -W 1 " + hostname + "> /dev/null")
        if response == 0:
            host = "is up!"

        logger.debug(f"Пинг {hostname} - {host}")
        await bot.send_message(callback.from_user.id, f"Switch: {hostname} {host}",
                               reply_to_message_id=callback.message.message_id)
        return True

    await bot.send_message(callback.from_user.id, f"value: {post['value']}\naction: {post['action']}\n\n{post}")


@dp.message_handler(filters.IDFilter(user_id=conf.misc.users), content_types=types.ContentType.PHOTO)
async def scan_message(message: types.Message):
    device: Any
    db = pymysql.connect(host=conf.db.host,
                         user=conf.db.user,
                         password=conf.db.password,
                         database=conf.db.database,
                         # cursorclass=pymysql.cursors.DictCursor
                         )

    if message.reply_to_message and re.match('^\\d{5}$', message.reply_to_message.text):
        is_exist = False
        asset_tag = re.search('^\\d{5}$', message.reply_to_message.text)
        asset_tag = str(asset_tag[0])

        try:
            device = nb.dcim.devices.get(asset_tag=asset_tag)
        except pynetbox.RequestError as e:
            pprint(e.error)
            device = False

        filename = asset_tag + '-' + message.photo[-1].file_unique_id + '.jpg'
        text_out = (f"Инв № - {asset_tag}\n"
                    f"Файл - {filename}\n"
                    f"Отправил - {message.reply_to_message.from_user.first_name}\n"
                    )
        logger.debug(f"!!!!!!! switch = {device}")
        if device:
            text_out += f"Netbox - {device.id}"
        else:
            text_out += f"Netbox - нет"

        select_all_rows = f"SELECT * FROM `bot_photo` WHERE tid='{message.photo[-1].file_unique_id}' AND sid='{asset_tag}' LIMIT 1"
        with db.cursor() as cursor:
            cursor.execute(select_all_rows)
            row = cursor.fetchone()

        if not row:
            args = (asset_tag, filename, message.photo[-1].file_unique_id, message.photo[-1].file_id,
                    message.reply_to_message.from_user.first_name)
            insert_query = f"INSERT INTO `bot_photo` (`sid`, `name`, `tid`, `file_id`, `upload`) VALUES (%s, %s, %s, %s, %s);"
            query_insert(insert_query, args)
            is_exist = True
        logger.debug(f"is_exist = {is_exist}")

        await message.photo[-1].download(destination_file=conf.tg_bot.upload_dir_photo + filename)
        destination = conf.tg_bot.upload_dir_photo + filename
        image_id = message.photo[len(message.photo) - 1].file_id
        file_path = (await bot.get_file(image_id)).file_path
        await bot.download_file(file_path, destination)

        keyboard = InlineKeyboardMarkup(row_width=3)
        if device.id:
            keyboard.add(InlineKeyboardButton(text="Device", url=device.url.replace('/api/', '/')))
            keyboard.add(
                InlineKeyboardButton(text="Фото", callback_data=cb.new(action="photo", value=device.id, id='')))
            keyboard.add(InlineKeyboardButton(text="Залить", callback_data=cb.new(action="upload",
                                                                                  value=device.id,
                                                                                  id=filename)))

        if is_exist:
            # if message.from_user.id != 252810436:
            await bot.send_photo('252810436', message.photo[-1]["file_id"], caption=text_out, reply_markup=keyboard)
            await bot.send_message(message.from_user.id, f"Принято {filename}",
                                   reply_to_message_id=message.reply_to_message)
        else:
            await message.answer("Такое фото уже есть в базе")
    else:
        await message.answer("Фотография должна быть ответом на Инв свича")
    db.close()


def iterate_devices(device):
    match device.status.value:
        case 'active':
            status = '🟢'
        case 'offline':
            status = '🔴'
        case 'inventory':
            status = '📦'
        case 'decommissioning':
            status = '⚰️'
        case _:
            status = device.status.value

    try:
        hostname = ipaddress.ip_interface(device.primary_ip4)
        hostname = str(hostname.ip)
    except ValueError:
        hostname = None

    msg = (
        f"<b>Адрес:</b> {device.site}\n"
        f"<b>Стойка:</b> {device.rack}\n\n"
        f"<b>Имя:</b> {device.name} {status}\n"
        f"<b>Инв </b>: {device.asset_tag}\n"
        f"<b>Модель:</b> {device.device_type}\n"
        f"<b>IP:</b> {hostname}\n"
        f"<b>NetboxID:</b> {device.id}\n"
        f"<b>Контакты:</b> {device.custom_fields['Contact']}\n"
        f"<b>Comment:</b>\n\n<pre>{device.comments}</pre>"
    )

    buttons = [
        types.InlineKeyboardButton(text="Device", url=device.url.replace('/api/', '/')),
        types.InlineKeyboardButton(text="Ping", callback_data=cb.new(action="ping", value=device.id, id='')),
        types.InlineKeyboardButton(text="Фото", callback_data=cb.new(action="photo", value=device.id, id=''))
    ]
    # logger.debug(f"{device.id}")
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)

    return msg, keyboard


@dp.message_handler(filters.IDFilter(user_id=conf.misc.users))
async def echo(message: types.Message):
    if len(message.text) < 5:
        await message.answer("Запрос должен быть длиннее")
        return False
    devices = ''
    sites = ''

    if re.match('^\\d{5}$', message.text) or re.match('^0\\d{4}$', message.text):
        text = re.match('^\\d{5}$', message.text) or re.match('^0\\d{4}$', message.text)
        devices = nb.dcim.devices.get(asset_tag=text[0])
        cnt = nb.dcim.devices.count(asset_tag=text[0])
    elif re.search("^[0-9a-zA-Z_-]*$", message.text):
        text = re.match('^[0-9a-zA-Z_-]*$', message.text)
        devices = nb.dcim.devices.filter(name__ic=text[0], role_id={2, 3, 4})
        # cnt = nb.dcim.devices.count(name__ic=text[0], role_id={2, 3, 4})
        cnt = False
    else:
        sites = nb.dcim.sites.filter(name__ic=message.text)
        cnt = nb.dcim.sites.count(name__ic=message.text)
    if cnt == 1:
        msg, key = iterate_devices(devices)
        await message.answer(msg, reply_markup=key, parse_mode='HTML')
    elif cnt is False:
        for device in devices:
            msg, key = iterate_devices(device)
            # pprint(device.name)
            await message.answer(msg, reply_markup=key, parse_mode='HTML')
            time.sleep(0.5)
    elif cnt > 1:
        for site in sites:
            devices = nb.dcim.devices.filter(site_id=site.id, role_id={2, 3, 4})
            # pprint(site)
            for device in devices:
                msg, key = iterate_devices(device)
                await message.answer(msg, reply_markup=key, parse_mode='HTML')
                time.sleep(0.5)
    else:
        await message.answer("Ничего не найдено")
