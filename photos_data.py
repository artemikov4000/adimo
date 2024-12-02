import requests
import json
from datetime import datetime
import math

token = 'b5355eeab5355eeab5355eea61b62be318bb535b5355eead3dbde708404b5d05420abaf'

def get_vk_id(username):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': username,
        'access_token': token,
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'response' in data and len(data['response']) > 0:
        return data['response'][0]['id']
    else:
        print("Пользователь не найден.")
        return None


def get_album(vk_id):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': vk_id,
        'access_token': user_token,
        'extended': 0,
        'count': 15,
        'v': '5.131',
        'album_id' : 'wall'
    }
    response = requests.get(url, params=params).json()
    photos = response['response']['items']
    photos_list = []
    for photo in photos:
        photos_list.append(photo['id'])
    return photos_list


def get_photos(vk_id, photos):
    url = 'https://api.vk.com/method/photos.get'
    for photo in photos:
        params = {
            'photos': photo,
            'access_token': token,
            'extended': 1,
            'v': '5.131',
        }
        response = requests.get(url, params=params).json()
        print(response)
    return


username = 'vladddac'

vk_id = get_vk_id(username)
print(vk_id)

if vk_id is not None:
    photos = get_album(vk_id)
    print(photos)
    get_photos(vk_id, photos)
