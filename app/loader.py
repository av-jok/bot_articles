from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import pymysql
from app.config import conf


bot = Bot(
    token=conf.tg_bot.token,
    parse_mode=types.ParseMode.HTML,
)

try:
    db = pymysql.connect(host=conf.db.host,
                         user=conf.db.user,
                         password=conf.db.password,
                         database=conf.db.database,
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        pass

    finally:
        # db.close()
        print("successfully connected...")
        print("#" * 20)

except Exception as ex:
    print("Connection refused...")
    print(ex)

storage = RedisStorage2(host=conf.redis.host, db=conf.redis.database) if conf.tg_bot.use_redis else MemoryStorage()

dp = Dispatcher(
    bot=bot,
    storage=storage,
)

# bot.delete_webhook(drop_pending_updates=True)

__all__ = (
    "bot",
    "storage",
    "dp",
)
