import requests
import json
from datetime import datetime
import math
import time

token = 'b5355eeab5355eeab5355eea61b62be318bb535b5355eead3dbde708404b5d05420abaf'
#usertoken = 'vk1.a.Fo49vYHDJ1TievPHiR7ROQiO3hmIzm1UOd4MZKBLqf6yfx0AlEkdyNC8Yw8Jmz9cTntsi0IokPNHyUFKMjEu6YF8bCjfPrSIMdqCqIguo4xRSwMlE9QzXvncewP6NsImZqOZrL8oM49NhLcGkjg4FZ33IMjfD28BH8EnZDg1XHkYaao7R182Wkclj4nuC1qnCVnFBAW4rtfgyPmlG7-H7A'
#usertoken = 'vk1.a.fY5EOPDReJBEcYOt3N6xkVtTPPaLe43XDeLkn3AgO5n1042_s3PxPs3ugaWKoYOHlrdkgjz4cqDyFKf-wlcCKoXydb64ESX4uk-_6W7XB6GKzVH5852sWsEsAUbPNU6qw-qNvFA3KVT1C0r3JVVNtQ1mqHCz8iC7_u973PI6jrRHYvBpegqW-v8AZ_8BthwNF3Ib8d33RvTrwGQysqdcbw'
usertoken = 'vk1.a.NbIn216Q5CV12LSTZRpabjlVwbn8s4McehTQaOkGmDeJVd-jsr8jNISh4klPi7Jk3TJseYgmkkgBGAdGboASkgKC0g5C7OfMB63alx5DPkQJG_9m_27KeT9aRc2C226qyYrtZB0EShLSXWT8LiORfJk-wqJtXY1ILqBe7Ql43pENsetMV4dAeLUeh5Cxc28NdxjZuqUyH8QuyusAvEp35w'

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


def get_album(vk_id):
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': vk_id,
        'access_token': user_token,
        'extended': 1,
        'count': 15,
        'v': '5.131',
        'album_id' : 'wall'
    }
    response = requests.get(url, params=params).json()
    photos = response['response']['items']
    photos_list = ''
    for photo in photos:
        # print(photo)
        photos_list += str(photo['id']) + ' , ' + photo['orig_photo']['url'] + ' , ' + photo['text'] + ' , ' + str(photo['likes']['count']) + '\n'
        # photo['orig_photo']['url']
        # photo['text']
        # photo['likes']['count']
        # photos_list.append(photo_info)
    return photos_list


def get_photos(vk_id, photos):
    url = 'https://api.vk.com/method/photos.getById'
    for photo in photos:
        time.sleep(1)
        id = f'{vk_id}_{photo}'
        print(id)
        params = {
            'photos': f'{id}',
            'access_token': token,
            'extended': 1,
            'v': '5.131',
        }
        response = requests.get(url, params=params)
        print(response.text)
        response = response.json()
        response = response['response'][0]
        url = response['orig_photo']['url']
        print(url)
        text = response['text']
        print(text)
        likes = response['likes']['count']
        print(likes)
    return


# 3 метода, для получения подписок на людей

def get_user_subscriptions(vk_id, access_token):
    url = 'https://api.vk.com/method/users.getSubscriptions'
    params = {
        'user_id': vk_id,
        'extended': 1,  # Для получения дополнительной информации о подписках
        'count': 200,  # Максимальное количество подписок для получения
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()
    print(response)

    if 'response' in response:
        return response['response']['items']
    return []

def get_user_info(user_id, access_token):
    url = 'https://api.vk.com/method/users.get'
    params = {
        'user_ids': user_id,
        'fields': 'nickname,domain,photo_50',  # Дополнительные поля для получения
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params).json()
    print(response)
    if 'response' in response and len(response['response']) > 0:
        user = response['response'][0]
        first_name = user.get('first_name', 'Имя не найдено')
        last_name = user.get('last_name', 'Фамилия не найдена')
        nickname = user.get('nickname', 'Никнейм не найден')
        domain = user.get('domain', 'Домен не найден')

        return {
            'id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'nickname': nickname,
            'domain': domain,
        }
    return None

# Посты пользователя



def get_subscriptions_info(vk_id, access_token):
    subscriptions = get_user_subscriptions(vk_id, access_token)
    subscriptions_info = []

    for subscription in subscriptions:
        time.sleep(1)
        if subscription['type'] == 'profile':  # Проверяем, что это подписка на пользователя
            user_id = subscription['id']
            user_info = get_user_info(user_id, access_token)
            if user_info:
                name = f"{user_info['first_name']} {user_info['last_name']}"
                description = user_info['domain']
                subscriptions_info.append({
                    'name': (user_id, name),
                    'description': description
                })
        elif subscription['type'] == 'page':  # Проверяем, что это подписка на группу
            group_id = subscription['id']
            name, description = get_group_info(group_id, access_token)
            if name and description:
                subscriptions_info.append({
                    'name': name,
                    'description': description
                })

    return subscriptions_info




# 3 метода, для получения груп, информации о группах и о каждой группе

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

def get_friends_info(vk_id, access_token):
    url = 'https://api.vk.com/method/friends.get'
    params = {
        'user_id': vk_id,
        'fields': 'city,education,occupation',  # Запрашиваем город, образование и работу
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(url, params=params)

    # Проверка статуса ответа
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        print(response.text)
        return

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        print(f"Response text: {response.text}")
        return

    # Проверка наличия ошибки в ответе
    if 'error' in response_json:
        print(f"API Error: {response_json['error']}")
        return

    # Обработка успешного ответа
    try:
        friends = response_json['response']['items']
        for friend in friends:
            friend_id = friend.get('id')
            city = friend.get('city', {}).get('title', 'Не указан')
            education = friend.get('university_name', 'Не указано')
            job = friend.get('occupation', {}).get('name', 'Не указано')

            print(f"ID: {friend_id}")
            print(f"Город: {city}")
            print(f"Образование: {education}")
            print(f"Работа: {job}")
            print("-" * 40)
    except KeyError as e:
        print(f"KeyError: {e}")
        print(f"Response data: {response_json}")

    return

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



if __name__ == "__main__":
    access_token = token  # Замените на ваш токен доступа
    user_token = usertoken
    username = 'vladddac'

    vk_id = get_vk_id(username, access_token)

    if vk_id is not None:

        friends_count = get_friends_count(vk_id, access_token)
        if friends_count is not None:
            print(f"Количество друзей у пользователя {username}: {friends_count}")
            # INT

        bdate = get_date_of_birth(vk_id, access_token)
        if bdate is not None:
            print(f"Дата рождения {username}: {bdate}")
            print(f"Возраст пользователя: {get_age(bdate)}")
            # Datetime
            # INT

        #AvLikes = get_average_likes_photos(vk_id, access_token)
        #if AvLikes is not None:
        #    print(f"Среднее количество лайков на фото: {math.floor(AvLikes)}")
        # INT

        #AvLikesp = get_average_likes_posts(vk_id, access_token)
        #if AvLikesp is not None:
        #    print(f"Среднее количество лайков на постах: {math.floor(AvLikesp)}")
        # INT

        #Interests = get_interests(vk_id, access_token)
        #if Interests is not None:
        #    print(f"Интересы пользователей: {Interests}")

        # Деятеьность String, Любимая музыка String, ЛЮюбимый фильм String
        # Любимое ТВ Шоу String, Любимые книги String, Любимые игры String
        # О себе String

        PostCount = get_posts_count(vk_id, access_token)
        if PostCount is not None:
            print(f"Количество постов: {PostCount}")

        # INT

        PhotoCount = get_photo_count(vk_id, access_token)
        if PhotoCount is not None:
            print(f"Количество фото: {PhotoCount}")

        # INT

        # Пользовательский токен


        # Выводим информацию о подписках на людей

        #subscriptions_info = get_subscriptions_info(vk_id, user_token)

        # Выводим информацию о каждой подписке
        #for subscription in subscriptions_info:
         #   print(f"ID: {subscription['name'][0]}") # INT
          #  print(f"Название/Имя: {subscription['name'][1]}") # String
           # print(f"Описание/Домен: {subscription['description']}") # String
            #print('-' * 40)

    photos = get_album(vk_id)
    print(photos)
    # get_photos(vk_id, photos)
    get_friends_info(vk_id, access_token)


