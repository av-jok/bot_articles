from dataclasses import dataclass
from environs import Env
from sqlalchemy import create_engine


# List of commands
commands = (
    ("start", "See if the ship is sailing"),
    ("help", "Get the command list"),
    ("ip", "Проверка по IP адресу"),
    ("file", "Загрузка фото на сервер"),
    ("reg", "Get the command list"),
    ("id", "Get the command list"),
)

env = Env()
env.read_env()

USERS = {52384439, 539181195, 345467127, 252810436, 347748319, 494729634, 1016868504, 361955359, 1292364914, 449155597,
         233703468, 842525963, 564569131, 1034083048, 224825221, 1369644834, 150862960, 1134721808, 1285798322, 700520296, 700520296}

PAYLOAD = ''
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
}

engine = create_engine("mysql+pymysql://root:pass@localhost/mydb")
# engine.connect()


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class RediConf:
    host: str
    password: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    skip_updates: bool


@dataclass
class Miscellaneous:
    other_params: str = None
    netbox_url: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RediConf
    misc: Miscellaneous


def load_config():

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("SUPERUSER_IDS"))),
            use_redis=env.bool("USE_REDIS"),
            skip_updates=env.bool("SKIP_UPDATES")
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        redis=RediConf(
            host=env.str('REDIS_HOST'),
            password=env.str('REDIS_PASSWORD'),
            database=env.str('REDIS_DATABASE')
        ),
        misc=Miscellaneous(
            netbox_url=env.str('NETBOX_URL')
        )

    )


conf = load_config()
