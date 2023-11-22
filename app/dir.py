import os
# import re
import pymysql
from app.config import conf

db = pymysql.connect(host=conf.db.host,
                     port=conf.db.port,
                     user=conf.db.user,
                     password=conf.db.password,
                     database=conf.db.database,
                     cursorclass=pymysql.cursors.DictCursor
                     )
db.autocommit(True)


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
    cursor.execute("SELECT `id`, `name` FROM `bot_photo`")
    rows = cursor.fetchall()

# rows = {}
results = diff_dir_with_array(conf.tg_bot.upload_dir_photo, rows)
for i in results:
    print(f"Файл существует, нет в базе {i}")

    # blob_value = open(f"{conf.tg_bot.upload_dir_photo}{i}", "rb").read()
    # text = re.search('^\\d{5}', i)
    # pprint(text[0])
    # sql = f"INSERT INTO test.bot_photo(`sid`, `name`) VALUES(%s, %s);"
    # args = (text[0], i)
    # with db.cursor() as cursor:
    #     cursor.execute(sql, args)
    # db.commit()

results = diff_array_with_dir(conf.tg_bot.upload_dir_photo, rows)
with db.cursor() as cursor:
    for i in results:
        print(f"В базе существует, нет файла {i}")
        cursor.execute(f"DELETE FROM test.bot_photo WHERE `name`='{i}'")
db.commit()
