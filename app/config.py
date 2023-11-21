import os
from dataclasses import dataclass
from typing import Any
from environs import Env
import pynetbox
import urllib3

# List of commands
commands = (
    ("start", "See if the ship is sailing"),
    ("help", "Get the command list"),
    ("id", "Get the command list"),
)

env = Env()
env.read_env()

USERS = {52384439, 539181195, 345467127, 252810436, 347748319, 494729634, 1016868504, 361955359, 1292364914, 449155597,
         233703468, 842525963, 564569131, 1034083048, 224825221, 1369644834, 150862960, 1134721808, 1285798322,
         700520296, 700520296}


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
    port: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    skip_updates: bool
    upload_dir_photo: str
    upload_dir_data: str
    upload_dir_rack: str


@dataclass
class NetBox:
    netbox_url: str = None
    netbox_api: str = None
    netbox_login: str = None
    netbox_pass: str = None


@dataclass
class Miscellaneous:
    other_params: str = None
    users: set[int | Any] = None
    headers: dict = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RediConf
    netbox: NetBox
    misc: Miscellaneous


def load_config():
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("SUPERUSER_IDS"))),
            use_redis=env.bool("USE_REDIS"),
            skip_updates=env.bool("SKIP_UPDATES"),
            upload_dir_photo=os.path.dirname(os.path.realpath(__file__)) + "/_Photos/",
            upload_dir_data=os.path.dirname(os.path.realpath(__file__)) + "/_Data/",
            upload_dir_rack=os.path.dirname(os.path.realpath(__file__)) + "/_Rack/"
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
            database=env.str('REDIS_DATABASE'),
            port=env.str('REDIS_PORT', 6379)
        ),
        netbox=NetBox(
            netbox_api=env.str('NETBOX_API'),
            netbox_url=env.str('NETBOX_URL'),
            netbox_login=env.str('NETBOX_LOGIN'),
            netbox_pass=env.str('NETBOX_PASS')
        ),
        misc=Miscellaneous(
            users=USERS,
            headers={'Content-Type': 'application/json', 'Authorization': f'Token {conf.netbox.netbox_api}'}
        )
    )


conf = load_config()
urllib3.disable_warnings()
nb = pynetbox.api(url=conf.netbox.netbox_url, token=conf.netbox.netbox_api)
nb.http_session.verify = False

# HEADERS = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Token {conf.netbox.netbox_api}'
# }
