import requests


def upload_photo():
    url = 'https://netbox.avantel.ru'
    ids = "12139"

    client = requests.session()
    client.get(url)
    csrftoken = client.cookies['csrftoken']
    login_data = dict(
        username="a.deripasko",
        password="5sMoeot92P4",
        csrfmiddlewaretoken=csrftoken,
        next=f"/extras/image-attachments/add/?content_type=19&object_id={ids}"
    )
    r = client.post(f"{url}/login/", data=login_data, headers=dict(Referer=url))

    csrftoken = r.cookies['csrftoken']
    res = client.get(
        f"{url}/extras/image-attachments/add/?content_type=19&object_id={ids}",
        data={'csrftoken': csrftoken, 'csrfmiddlewaretoken': csrftoken},
        headers=dict(Referer=url)
    )

    csrftoken = res.cookies['csrftoken']
    res = client.post(
        f"{url}/extras/image-attachments/add/?content_type=19&object_id={ids}",
        files={'image': open('joker.png', 'rb')},
        data={'name': '', 'csrfmiddlewaretoken': csrftoken},
        headers=dict(Referer=url)
    )
    return res.status_code


print(upload_photo())
