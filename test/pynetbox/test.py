import logging
import os
from pprint import pprint
import pynetbox
import requests
import urllib3

netbox_url = 'https://netbox.avantel.ru/'
netbox_api = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False

NETBOX_URL = 'https://netbox.avantel.ru/'
NETBOX_TOKEN = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'

nb = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)
nb.http_session.verify = False

# def update_images(deviceTypeId, img):
#     url = NETBOX_URL + f"api/dcim/device-types/{deviceTypeId}/"
#     headers = {"Authorization": f"Token {NETBOX_TOKEN}"}
#     files = {i: (os.path.basename(f), open(f, "rb"))
#              for i, f in img.items()}
#     response = requests.patch(url, headers=headers, files=files)
#     print(f'Images {img} updated at {url}: {files}')
#
#
# all_device_types = {item: item for item in nb.dcim.device_types.all()}
# for device_type in all_device_types:
#     images = {}
#     os.makedirs("images/" + str(device_type), exist_ok=True)
#     if os.path.exists("images/" + str(device_type) + "/f.jpg"):
#         images['front_image'] = "images/" + str(device_type) + "/f.jpg"
#     if os.path.exists("images/" + str(device_type) + "/r.png"):
#         images['rear_image'] = "images/" + str(device_type) + "/r.png"
#     if len(images) > 0:
#         print('Uploading images for' + str(device_type))
#         update_images(device_type.id, images)
#
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

image_data2 = dict(
    content_type="dcim.device",
    object_id=12139,
    name="Test image",
    image={(os.path.basename("joker.png"), open("joker.png", "rb"))},
    image_height=512,
    image_width=512,
)

try:
    nb.extras.image_attachments.create(image_data2)
except pynetbox.RequestError:
    logging.exception(f"Failed to attach image")
except TypeError:
    logging.exception(f"Failed to attach image")

pprint(dict(image_data2))

# try:
#     switch = nb.dcim.devices.get(asset_tag='99999')
# except pynetbox.RequestError as e:
#     pprint(e.error)
#     switch = False
#
# if switch:
#     print(switch.id)
