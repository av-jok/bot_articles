from loguru import logger

from .errors import retry_after
from .private import start
from .private import help
from .private import reg
from .private import any

logger.info("Handlers are successfully configured")
