from loguru import logger

from .errors import retry_after
from .private import start
from .private import help
from .private import reg

logger.info("Handlers are successfully configured")
