import os
import re
import ipaddress
from dataclasses import dataclass
from environs import Env
from requests import request
from typing import Union
import pynetbox
import pymysql
import urllib3
# from aiogram import types
# from pprint import pprint

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
         233703468, 842525963, 564569131, 1034083048, 224825221, 1369644834, 150862960, 1134721808, 1285798322,
         700520296, 700520296}

upload_dir_photo = os.path.dirname(os.path.realpath(__file__)) + "/_Photos/"
upload_dir_data = os.path.dirname(os.path.realpath(__file__)) + "/_Data/"
upload_dir_rack = os.path.dirname(os.path.realpath(__file__)) + "/_Rack/"

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
}

# engine = create_engine("mysql+pymysql://root:pass@localhost/mydb")
# engine.connect()


# class DB:
#     conn = None
#
#     def connect(self):
#         self.conn = pymysql.connect(host=conf.db.host,
#                                     user=conf.db.user,
#                                     password=conf.db.password,
#                                     database=conf.db.database,
#                                     cursorclass=pymysql.cursors.DictCursor
#                                     )
#         self.conn.autocommit(True)
#
#     def query(self, sql):
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute(sql)
#         except (AttributeError, pymysql.Error):
#             self.connect()
#             cursor = self.conn.cursor()
#             cursor.execute(sql)
#         return cursor


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
class NetBox:
    netbox_url: str = None
    netbox_api: str = None


@dataclass
class Miscellaneous:
    other_params: str = None


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
        netbox=NetBox(
            netbox_api=env.str('NETBOX_API'),
            netbox_url=env.str('NETBOX_URL')
        ),
        misc=Miscellaneous()
    )


conf = load_config()
urllib3.disable_warnings()
nb = pynetbox.api(url=conf.netbox.netbox_url, token=conf.netbox.netbox_api)
nb.http_session.verify = False


def query_select(query):
    try:
        base = pymysql.connect(host=conf.db.host,
                               user=conf.db.user,
                               password=conf.db.password,
                               database=conf.db.database,
                               cursorclass=pymysql.cursors.DictCursor
                               )
        base.autocommit(True)
        try:
            with base.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
        finally:
            base.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)
    return rows


class Switch:
    """Заполняет данные по свичам"""
    db: None
    id: int
    nid: int
    name: str
    device_type: str
    rack: str
    status: str
    ip: ipaddress
    address: str
    msg = Union[str, int]
    json = str
    url = str
    comments = str
    images: list

    def __init__(self):
        self.db = None

    def __call__(self, msg: str):
        url = conf.netbox.netbox_url + "api/dcim/devices/" + str(msg) + "/"
        response = request("GET", url, headers=HEADERS, data='')

        json = response.json()

        # pprint(json['count'])
        self.nid = json['id']
        self.name = json['name'].lower()
        self.device_type = json['device_type']['display']
        self.address = json['site']['display']

        if json['asset_tag']:
            asset_tag = re.findall(r"(?<!\d)\d{5}(?!\d)", json['asset_tag'])
            self.id = int(asset_tag[0])
        else:
            self.id = 0

        if json['rack'] is not None:
            self.rack = json['rack']['name']
        else:
            self.rack = ' '

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
        url = conf.netbox.netbox_url + "api/extras/image-attachments/?object_id=" + str(self.nid)
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
            return None

    def get_photo_in_base(self):
        # with self.db.cursor() as cursor:
        select_all_rows = f"SELECT `sid` as pid, `name`, `file_id` as image FROM `bot_photo` WHERE sid='{self.id}'"
        rows = query_select(select_all_rows)
        # cursor.execute(select_all_rows)
        # rows = cursor.fetchall()

        if rows:
            return rows
        else:
            return None
