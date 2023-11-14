import os
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

# sql = f"INSERT INTO `bot_photo` (sid, name, tid, file_id) VALUES ('{text}', '{filename}', '{message.photo[-1].file_unique_id}', '{message.photo[-1].file_id}');"
# cursor.execute(sql)
# db.commit()

results = diff_dir_with_array("/home/joker/git/bot_articles/app/_Photos/", rows)
for i in results:
    print(f"Файл существует, нет в базе {i}")
    replace(f"/home/joker/git/bot_articles/app/_Photos/{i}", f"/home/joker/old/{i}")
    # remove(f"/home/joker/sftp/app/_Photos/{i}")


results = diff_array_with_dir("/home/joker/git/bot_articles/app/_Photos", rows)
with db.cursor() as cursor:

    for i in results:
        print(f"В базе существует, нет файла {i}")
        cursor.execute(f"DELETE FROM test.bot_photo WHERE `name`='{i}'")
db.commit()
