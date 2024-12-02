import requests
import json
from datetime import datetime
import math

token = 'b5355eeab5355eeab5355eea61b62be318bb535b5355eead3dbde708404b5d05420abaf'
usertoken = 'vk1.a.Fo49vYHDJ1TievPHiR7ROQiO3hmIzm1UOd4MZKBLqf6yfx0AlEkdyNC8Yw8Jmz9cTntsi0IokPNHyUFKMjEu6YF8bCjfPrSIMdqCqIguo4xRSwMlE9QzXvncewP6NsImZqOZrL8oM49NhLcGkjg4FZ33IMjfD28BH8EnZDg1XHkYaao7R182Wkclj4nuC1qnCVnFBAW4rtfgyPmlG7-H7A'


def get_user_groups(vk_id, access_token):
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'user_id': vk_id,
        'extended': 1,  # Для получения дополнительной информации о группах
        'count': 200,  # Максимальное количество групп для получения
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()
    print(response)
    print(type(response))
    if 'response' in response:
        return response['response']['items']
    return []


def get_group_info(group_id, access_token):
    url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_id': group_id,
        'fields': 'description',  # Добавляем поле description для получения описания
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response and len(response['response']) > 0:
        group = response['response'][0]
        name = group.get('name', 'Название не найдено')
        description = group.get('description', 'Описание не найдено')
        NameIdPair = (group_id, name)
        return NameIdPair, description
    return None, None


def get_groups_info(vk_id, access_token):
    groups = get_user_groups(vk_id, access_token)
    groups_info = []

    for group in groups:
        group_id = group['id']
        name, description = get_group_info(group_id, access_token)
        if name and description:
            groups_info.append({
                'name': name,
                'description': description
            })

    return groups_info


def get_vk_id(username, access_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': username,
        'access_token': access_token,
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'response' in data and len(data['response']) > 0:
        return data['response'][0]['id']
    else:
        print("Пользователь не найден.")
        return None


# 3 метода, для получения груп, информации о группах и о каждой группе


def get_group_info(group_id, access_token):
    url = 'https://api.vk.com/method/groups.getById'
    params = {
        'group_id': group_id,
        'fields': 'description',  # Добавляем поле description для получения описания
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response and len(response['response']) > 0:
        group = response['response'][0]
        name = group.get('name', 'Название не найдено')
        description = group.get('description', 'Описание не найдено')
        NameIdPair = (group_id, name)
        return NameIdPair, description
    return None, None


# Метод, выводящий возраст пользователя

def get_age(bdate):
    birth_date = datetime.strptime(bdate, '%d.%m.%Y')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


# Метод возвращающий среднее количество лайков на постах

def get_average_likes_posts(vk_id, access_token):
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': vk_id,
        'count': 100,  # Максимальное количество постов для расчета
        'extended': 1,  # Для получения количества лайков
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response and 'items' in response['response']:
        posts = response['response']['items']
        total_likes = sum(post['likes']['count'] for post in posts)
        average_likes = total_likes / len(posts) if posts else 0
        return average_likes
    return None

# Метод возвращающий среднее количество лайков на фото

def get_average_likes_photos(vk_id, access_token):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': vk_id,
        'album_id': 'profile',
        'extended': 1,  # Для получения количества лайков
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response and 'items' in response['response']:
        photos = response['response']['items']
        total_likes = sum(photo['likes']['count'] for photo in photos)
        average_likes = total_likes / len(photos) if photos else 0
        return average_likes
    return None

# Интересы пользователей

def get_interests(vk_id, access_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': vk_id,
        'fields': 'activities,interests,music,movies,tv,books,games,about',
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response and len(response['response']) > 0:
        user = response['response'][0]
        interests = []
        if 'activities' in user and user['activities']:
            interests.append(f"Деятельность: {user['activities']}")
        if 'interests' in user and user['interests']:
            interests.append(f"Интересы: {user['interests']}")
        if 'music' in user and user['music']:
            interests.append(f"Любимая музыка: {user['music']}")
        if 'movies' in user and user['movies']:
            interests.append(f"Любимые фильмы: {user['movies']}")
        if 'tv' in user and user['tv']:
            interests.append(f"Любимые телешоу: {user['tv']}")
        if 'books' in user and user['books']:
            interests.append(f"Любимые книги: {user['books']}")
        if 'games' in user and user['games']:
            interests.append(f"Любимые игры: {user['games']}")
        if 'about' in user and user['about']:
            interests.append(f"О себе: {user['about']}")

        return '; '.join(interests)
    return None


# Метод возвращающий кол - во постов

def get_posts_count(vk_id, access_token):
    url = 'https://api.vk.com/method/wall.get'
    params = {
        'owner_id': vk_id,
        'count': 0,  # Не нужно получать посты, только количество
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response:
        return response['response']['count']
    return None

# Метод возвращающий дату рождения

def get_date_of_birth(vk_id, access_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': vk_id,
        'fields': 'bdate',
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response and len(response['response']) > 0:
        user = response['response'][0]
        if 'bdate' in user:
            return user['bdate']
    return None

# Метод, возвращающий количество фото на странице

def get_photo_count(vk_id, access_token):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': vk_id,
        'album_id': 'profile',
        'count': 0,  # Не нужно получать фотографии, только количество
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()

    if 'response' in response:
        count = response['response']['count']
        if count >= 15:
            return f">= 15"
        return count
    return None

# Метод, выводящий количество друзей и пользователя

def get_friends_count(vk_id, access_token):
    url = 'https://api.vk.com/method/friends.get'
    params = {
        'user_id': vk_id,
        'access_token': access_token,
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'response' in data:
        return data['response']['count']
    else:
        print("Не удалось получить список друзей.")
        return None


access_token = token  # Замените на ваш токен доступа
user_token = usertoken
username = 'vladddac'

vk_id = get_vk_id(username, access_token)

if vk_id is not None:
    friends_count = get_friends_count(vk_id, access_token)
    if friends_count is not None:
        print(f"Количество друзей у пользователя {username}: {friends_count}")

    bdate = get_date_of_birth(vk_id, access_token)
    if bdate is not None:
        print(f"Дата рождения {username}: {bdate}")
        print(f"Возраст пользователя: {get_age(bdate)}")

    #AvLikes = get_average_likes_photos(vk_id, access_token)
    #if AvLikes is not None:
    #    print(f"Среднее количество лайков на фото: {math.floor(AvLikes)}")

    #AvLikesp = get_average_likes_posts(vk_id, access_token)
    #if AvLikesp is not None:
    #    print(f"Среднее количество лайков на постах: {math.floor(AvLikesp)}")

    #Interests = get_interests(vk_id, access_token)
    #if Interests is not None:
    #    print(f"Интересы пользователей: {Interests}")

    PostCount = get_posts_count(vk_id, access_token)
    if PostCount is not None:
        print(f"Количество постов: {PostCount}")

    PhotoCount = get_photo_count(vk_id, access_token)
    if PhotoCount is not None:
        print(f"Количество фото: {PhotoCount}")

    # Пользовательский токен

    groups_info = get_groups_info(vk_id, user_token)
    for group in groups_info:
        print(f"ID сообщества: {group['name'][0]}")
        print(f"Название сообщества: {group['name'][1]}")
        print(f"Описание сообщества: {group['description']}")
        #print(f"id сообщества: {group['group_id']}")
        print('-' * 40)
        break