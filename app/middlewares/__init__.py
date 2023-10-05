from loguru import logger
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from .throttling import ThrottlingMiddleware, rate_limit
from .albummiddleware import AlbumMiddleware

from app.loader import dp

if __name__ == "app.middlewares":
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(AlbumMiddleware())

    logger.info('Middlewares are successfully configured')
