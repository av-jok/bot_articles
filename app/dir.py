import os
import re
import pymysql
from aiogram import types

from app.config import conf
from functools import wraps

db = pymysql.connect(host=conf.db.host,
                     user=conf.db.user,
                     password=conf.db.password,
                     database=conf.db.database,
                     cursorclass=pymysql.cursors.DictCursor
                     )
db.autocommit(True)

admins = [1, 2, 3]  # Telegram ids of admins (from your config)


def admins_only_handler(handler):
    @wraps(handler)
    def authorized_handler(message: types.Message, *args, **kwargs):
        if message.from_user.id in admins:
            return handler(message, *args, **kwargs)
        else:
            message.reply('You are not authorized to perform this action')

    return authorized_handler


# @admins_only_handler
def diff_dir_with_filelist(directory, filepath):
    new_files = os.listdir(directory)
    with open(filepath, 'r') as text_file:
        old_list = text_file.readlines()

    old_files = set(item.rstrip() for item in old_list)
    return [x for x in new_files if x not in old_files]


def diff_dir_with_array(directory, array):
    new_files = os.listdir(directory)
    old_files = []
    for row in array:
        old_files.append(row['name'])
    old_files = set(item.rstrip() for item in old_files)
    return [x for x in new_files if x not in old_files]


def diff_array_with_dir(directory, array):
    new_files = os.listdir(directory)
    old_files = []
    for row in array:
        old_files.append(row['name'])
    old_files = set(item.rstrip() for item in old_files)
    return [x for x in old_files if x not in new_files]


def replace(source, destination):
    try:
        os.rename(source, destination)
    except OSError as f:
        print(f)
        return


def remove(source):
    try:
        os.unlink(source)
    except OSError as f:
        print(f)
        return


with db.cursor() as cursor:
    cursor.execute("SELECT `id`, `name` FROM `bot_photo`")
    rows = cursor.fetchall()

# rows = {}
results = diff_dir_with_array(conf.tg_bot.upload_dir_photo, rows)
for i in results:
    print(f"Файл существует, нет в базе {i}")
    # replace(f"/home/joker/git/bot_articles/app/_Photos/{i}", f"/home/joker/old/{i}")
    # remove(f"/home/joker/sftp/app/_Photos/{i}")

    # blob_value = open(f"{conf.tg_bot.upload_dir_photo}{i}", "rb").read()
    # text = re.search('^\\d{5}', i)
    # pprint(text[0])
    # sql = f"INSERT INTO test.bot_photo(`sid`, `name`) VALUES(%s, %s);"
    # args = (text[0], i)
    # with db.cursor() as cursor:
    #     cursor.execute(sql, args)
    # db.commit()


results = diff_array_with_dir(conf.tg_bot.upload_dir_photo, rows)
# with db.cursor() as cursor:
#
#     for i in results:
#         print(f"В базе существует, нет файла {i}")
#         cursor.execute(f"DELETE FROM test.bot_photo WHERE `name`='{i}'")
# db.commit()
