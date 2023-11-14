import os
import re
from pprint import pprint
from typing import Union

import pymysql
from app.config import conf

db = pymysql.connect(host=conf.db.host,
                     user=conf.db.user,
                     password=conf.db.password,
                     database=conf.db.database,
                     cursorclass=pymysql.cursors.DictCursor
                     )
db.autocommit(True)


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


with db.cursor() as cursor:
    cursor.execute("SELECT `name` FROM `bot_photo`")
    rows = cursor.fetchall()


# insert_query = f"INSERT INTO `bot_photo` (sid, name, tid, file_id) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}', '{message.photo[-1].file_id}');"
# query_insert(insert_query)
# base.commit()

results = diff_dir_with_array("/home/joker/git/bot_articles/app/_Photos", rows)
out = []

for i in results:
    print(f"Файл существует, нет в базе {i}")

results = diff_array_with_dir("/home/joker/git/bot_articles/sftp/app/_Photos", rows)
out = []

for i in results:
    print(f"В базе существует, нет файла {i}")
