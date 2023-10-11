import base64
import logging
import pynetbox
import urllib3
import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from pprint import pprint

netbox_url = 'https://netbox.avantel.ru/'
netbox_api = '7f50ada4a4a66d4b2385e4f8f59a069bc219089b'
urllib3.disable_warnings()

nb = pynetbox.api(url=netbox_url, token=netbox_api)
nb.http_session.verify = False


class ArticleBase64Serilizer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)


# devices = nb.dcim.devices.filter(asset_tag='17855')
# for device in devices:
#     pprint(device)
#     device.name = device.name.lower()
#     pprint(dict(device))


# img = nb.extras.image_attachments.filter(object_id='1')
# print(img.id)

# sites = nb.dcim.sites.filter(status='active', region_id='1')
# for site in sites:
#     site.name = site.name.lower()
#     pprint(dict(site))

def base64_image_upload_api_view(data):
    serializer = ArticleBase64Serilizer(data=data)
    data = serializer.initial_data
    return data


with open("joker.png", "rb") as file_handle:
    image_data = file_handle.read()
    # base_encoded = base64.b64encode(image_data).decode("utf8")
    image_data2 = dict(
        content_type="dcim.device",
        object_id=8593,
        name="Test image",
        image=image_data,
        image_height=512,
        image_width=512,
        )
    img = base64_image_upload_api_view(image_data2)
    pprint(img)
    try:
        nb.extras.image_attachments.create(img)
    except pynetbox.RequestError:
        logging.exception(f"Failed to attach image")
# pprint(dict(image_data))
