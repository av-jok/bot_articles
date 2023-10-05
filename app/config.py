import os
import re
import ipaddress
from dataclasses import dataclass
from environs import Env
from sqlalchemy import create_engine
from requests import request
# from aiogram import types
from pprint import pprint

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


upload_dir_photo = os.path.dirname(os.path.realpath(__file__)) + "/Photos/"
upload_dir_data = os.path.dirname(os.path.realpath(__file__)) + "/Data/"

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


class Switch:

    """Заполняет данные по свичам"""
    db: None
    id: int
    nid: int
    name: str
    device_type: str
    rack: None
    status: str
    ip: ipaddress
    address: str
    msg = str
    json = str
    url = str
    comments = str
    images: list

    def __init__(self, db):
        self.db = db

    def __call__(self, msg: str):
        url = conf.misc.netbox_url + "api/dcim/devices/" + str(msg) + "/"
        response = request("GET", url, headers=HEADERS, data='')

        json = response.json()

        # pprint(json['count'])
        self.nid = json['id']
        self.name = json['name'].lower()
        self.device_type = json['device_type']['display']

        if json['asset_tag']:
            asset_tag = re.findall(r'\d+', json['asset_tag'])
            self.id = int(asset_tag[0])
        else:
            self.id = 0

        if json['rack'] is not None:
            self.rack = json['rack']['name']
        else:
            self.rack = None

        self.status = json['status']['label']

        if json['primary_ip'] is not None:
            ip = json['primary_ip']['address'].split('/')
            self.ip = ip[0]
        else:
            self.ip = None
        self.url = json['url'].replace('/api/', '/')
        self.comments = json['comments']
        self.images = self.get_photo_in_netbox()
        self.images2 = self.get_photo_in_base()

        return self

    def get_photo_in_netbox(self):
        url = conf.misc.netbox_url + "api/extras/image-attachments/?object_id=" + str(self.nid)
        response = request("GET", url, headers=HEADERS, data='')
        json = response.json()
        photos = list()
        if json['count'] > 0:
            for iterator in json['results']:
                photos.append({
                    'pid': iterator['id'],
                    'image': iterator['image'],
                    'name': iterator['name'],
                    'object_id': iterator['object_id']}
                )
            return photos
        else:
            return False

    def get_photo_in_base(self):
        # TODO Доделать вывод фоток

        with self.db.cursor() as cursor:
            select_all_rows = f"SELECT `sid` as pid, `file_id` as image FROM `bot_photo` WHERE sid='{self.id}'"
            cursor.execute(select_all_rows)

            rows = cursor.fetchall()
            # for row in rows:
        return rows
