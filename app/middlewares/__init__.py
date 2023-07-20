from loguru import logger
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from .throttling import ThrottlingMiddleware, rate_limit

from app.loader import dp

if __name__ == "app.middlewares":
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(ThrottlingMiddleware())

    logger.info('Middlewares are successfully configured')
