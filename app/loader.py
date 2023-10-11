from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import pymysql
from app.config import conf

bot = Bot(
    token=conf.tg_bot.token,
    parse_mode=types.ParseMode.HTML,
)

db = pymysql.connect(host=conf.db.host,
                     user=conf.db.user,
                     password=conf.db.password,
                     database=conf.db.database,
                     cursorclass=pymysql.cursors.DictCursor)
db.autocommit(True)

storage = RedisStorage2(host=conf.redis.host, db=conf.redis.database) if conf.tg_bot.use_redis else MemoryStorage()

dp = Dispatcher(
    bot=bot,
    storage=storage,
)


def query_select(query):
    try:
        base = pymysql.connect(host=conf.db.host,
                               user=conf.db.user,
                               password=conf.db.password,
                               database=conf.db.database,
                               cursorclass=pymysql.cursors.DictCursor
                               )
        base.autocommit(True)
        try:

            with base.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        finally:
            base.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)
    return rows


def query_insert(query):
    is_true = None

    try:
        base = pymysql.connect(host=conf.db.host,
                               user=conf.db.user,
                               password=conf.db.password,
                               database=conf.db.database,
                               cursorclass=pymysql.cursors.DictCursor
                               )
        base.autocommit(True)
        try:
            with base.cursor() as cursor:
                cursor.execute(query)
                base.commit()
                is_true = True
        except Exception as ex:
            print(ex)
            is_true = False
        finally:
            base.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

    return is_true


# bot.delete_webhook(drop_pending_updates=True)


__all__ = (
    "bot",
    "storage",
    "dp",
    "db",
    "query_select",
    "query_insert",
)
