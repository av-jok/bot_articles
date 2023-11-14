import logging
from pprint import pprint

import pynetbox
import requests
import urllib3
from bs4 import BeautifulSoup

# from pprint import pprint


netbox_url = 'https://netbox.avantel.ru/'
netbox_api = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False

# i = 0
# devices = nb.dcim.sites.filter(region_id=1)  # asset_tag__ic='авантел', role_id=4, status='offline'
# for device in devices:
#     print(device, device.slug, transliterate(device.name))
#     device.slug = transliterate(device.name)
# if re.findall(r"(?<!\d)\d{5}(?!\d)", device.asset_tag):
#     text = re.findall(r"(?<!\d)\d{5}(?!\d)", device.asset_tag)
#     device.name = device.name.lower()
#     transliterate = transliterate(device.name)
#     device.asset_tag = text[0]
#     device.asset_tag = None
# try:
#     print(device, device.asset_tag, text)
# device.save()
# except pynetbox.RequestError as e:
#     print(device.asset_tag, e.error)

# if i == 5:
#     exit()
# i += 1

# img = nb.extras.image_attachments.filter(object_id='1')
# print(img.id)

# sites = nb.dcim.sites.filter(status='active', region_id='1')
# for site in sites:
#     site.name = site.name.lower()
#     pprint(dict(site))

# with open("joker.png", "rb") as file_handle:
#     image_data = file_handle.read()
#     base_encoded = base64.b64encode(image_data).decode("utf8")
#     image_data2 = dict(
#         content_type="dcim.device",
#         object_id=8593,
#         name="Test image",
#         image=base_encoded,
#         image_height=512,
#         image_width=512,
#         )
#
#     try:
#         nb.extras.image_attachments.create(image_data2)
#     except pynetbox.RequestError:
#         logging.exception(f"Failed to attach image")
# pprint(dict(image_data))

logging.debug('Run Auth')

url = 'https://netbox.avantel.ru/login/'
user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

session = requests.Session()
r = session.get(url, headers={
    'User-Agent': user_agent_val
})

res = session.get(url)
signin = BeautifulSoup(res.content, 'html.parser')
csrfmiddlewaretoken = signin.find(attrs={"name": "csrfmiddlewaretoken"}).get('value')

session.headers.update({'Referer': url})
session.headers.update({'User-Agent': user_agent_val})

ress = session.post(url, {
    'username': "a.deripasko",
    'password': "5sMoeot92P4",
    'next': "/dcim/devices/12139/",
    'csrfmiddlewaretoken': csrfmiddlewaretoken
})

# signin = BeautifulSoup(ress.content, 'html.parser')

files = {'image': open('joker.png', 'rb')}
values = {'name': '', 'csrfmiddlewaretoken': csrfmiddlewaretoken}

with session.post(
        f"https://netbox.avantel.ru/extras/image-attachments/add/?content_type=19&object_id=12139",
        files=files,
        data=values
) as res:
    signin = BeautifulSoup(res.content, 'html.parser')
    pprint(signin)
