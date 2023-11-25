import os
import urllib3
import pynetbox
from environs import Env
from dataclasses import dataclass

urllib3.disable_warnings()

# List of commands
commands = (
    ("start", "See if the ship is sailing"),
    ("help", "Get the command list"),
    ("id", "Get the command list"),
)


@dataclass
class DbConfig:
    host: str
    port: str
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
    user_ids: list[int]
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
            user_ids=list(map(int, env.list("USERS_IDS"))),
            use_redis=env.bool("USE_REDIS"),
            skip_updates=env.bool("SKIP_UPDATES"),
            upload_dir_photo=os.path.dirname(os.path.realpath(__file__)) + "/_Photos/",
            upload_dir_data=os.path.dirname(os.path.realpath(__file__)) + "/_Data/",
            upload_dir_rack=os.path.dirname(os.path.realpath(__file__)) + "/_Rack/"
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
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
            headers={'Content-Type': 'application/json', 'Authorization': f"Token {env.str('NETBOX_API')}"}
        )
    )


env = Env()
env.read_env()
conf = load_config()
nb = pynetbox.api(url=conf.netbox.netbox_url, token=conf.netbox.netbox_api)
nb.http_session.verify = False
urllib3.disable_warnings()
