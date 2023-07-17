from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from app import config
from app.config import load_config

conf = load_config("data/.env")

bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
)

storage = MemoryStorage()
storage = RedisStorage2(host=conf.redis.host, db=conf.redis.database) if conf.tg_bot.use_redis else MemoryStorage()

dp = Dispatcher(
    bot=bot,
    storage=storage,
)

__all__ = (
    "bot",
    "storage",
    "dp",
)
