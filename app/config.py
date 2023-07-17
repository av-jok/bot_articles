from pathlib import Path

from environs import Env

env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
WORK_PATH: Path = Path(__file__).parent.parent

SUPERUSER_IDS = env.list("SUPERUSER_IDS")

USERS = {52384439, 539181195, 345467127, 252810436, 347748319, 494729634, 1016868504, 361955359, 1292364914, 449155597,
         233703468, 842525963, 564569131, 1034083048, 224825221, 1369644834, 150862960, 1134721808, 1285798322}

PAYLOAD = ''
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
}